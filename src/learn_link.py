#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""learn_link.py — 用本地 Ollama 模型对 GitHub 热门做「学习 + 链接 + 知识图谱」。

流程：
  (a) 每日消化报告  reports/learnings/YYYY-MM-DD.md
  (b) 滚动 7 天「主题图谱（知识图谱）+ 本周趋势聚合」 knowledge-base/learn_links/WEEKLY.md
  (c) INDEX.md 重组为「图谱优先 + 本周趋势 + 每日摘要（按日期幂等）」，
      使累积知识库更像知识图谱而非流水摘要行。

仅依赖 Python 标准库（urllib 调 Ollama HTTP API）。Ollama 不可用时优雅跳过，
不阻断整个自动化（best-effort）。
"""
import os
import sys
import json
import re
import datetime
import subprocess
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
META_DIR = ROOT / "data" / "metadata"
LEARN_DIR = ROOT / "reports" / "learnings"
LINK_DIR = ROOT / "knowledge-base" / "learn_links"
LINK_INDEX = LINK_DIR / "INDEX.md"
WEEKLY_MD = LINK_DIR / "WEEKLY.md"
SUMMARY_JSON = LINK_DIR / "summaries.json"

OLLAMA_CHAT = "http://localhost:11434/api/chat"
OLLAMA_TAGS = "http://localhost:11434/api/tags"

# RAG 向量库（Milvus Lite + nomic-embed-text）：由 ~/rag_venv 下的脚本驱动，
# learn_link 通过 subprocess 调用，避免在主进程依赖 milvus_lite（仅装在该 venv）。
# Windows(win 分支) 上没有 ~/rag_venv，rag_retrieve/rag_ingest 自动降级为 no-op，不影响主流程。
RAG_VENV_PY = os.path.expanduser("~/rag_venv/bin/python")
RAG_SCRIPT_DIR = os.path.join(str(ROOT), "src")

# 模型偏好顺序：取本地 /api/tags 里第一个命中的，避免模型被删后 404 静默失败。
# 排序依据 GB10 实测：qwen3.8:27b（Q4_K_M，256K 上下文 + thinking/vision）综合最强，置顶；
# 其后按激活参数小者优先（qwen3-coder:30b ~82 tok/s 远快于 dense 32B/72B）。
MODEL_PREFERENCE = [
    "qwen3.8:27b",
    "qwen3-coder:30b",
    "qwen2.5-coder:32b",
    "qwen2.5-coder:14b",
    "qwen2.5:72b",
    "deepseek-r1:32b",
]


def _list_local_models():
    try:
        with urllib.request.urlopen(OLLAMA_TAGS, timeout=10) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
        return [m.get("name", "") for m in payload.get("models", [])]
    except Exception as exc:  # noqa
        print(f"[learn_link] 无法读取 Ollama 模型列表：{exc}", flush=True)
        return []


def _resolve_model():
    """LEARN_MODEL 显式指定优先；否则按偏好列表挑一个本地真实存在的模型。"""
    explicit = os.environ.get("LEARN_MODEL")
    local = _list_local_models()
    if explicit:
        if not local or explicit in local:
            return explicit
        print(
            f"[learn_link] LEARN_MODEL={explicit} 不在本地模型列表，回退自动选择",
            flush=True,
        )
    for cand in MODEL_PREFERENCE:
        if cand in local:
            return cand
    if local:
        return local[0]
    return explicit or MODEL_PREFERENCE[0]


MODEL = _resolve_model()
HTTP_TIMEOUT = int(os.environ.get("LEARN_TIMEOUT", "600"))
WEEK_DAYS = int(os.environ.get("LEARN_WEEK_DAYS", "7"))


def log(msg):
    ts = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[learn_link {ts}] {msg}", flush=True)


# ----------------------------------------------------------------------------
# 数据读取
# ----------------------------------------------------------------------------
def _proj_info(item):
    """从 metadata 条目里尽量稳健地抽出项目核心字段。"""
    p = item.get("project") or item.get("repo") or {}
    full = p.get("full") or p.get("name") or item.get("full") or "?"
    lang = p.get("language") or item.get("language") or "?"
    stars = p.get("stars") or item.get("stars") or 0
    cats = p.get("categories") or item.get("categories") or []
    if isinstance(cats, str):
        cats = [cats]
    desc = p.get("description") or item.get("description") or ""
    status = item.get("install") or item.get("status") or item.get("run") or ""
    return full, lang, stars, cats, desc, status


def load_day(date):
    main_data, board_data = [], []
    main_path = META_DIR / f"{date.isoformat()}.json"
    board_path = META_DIR / f"{date.isoformat()}-boards.json"
    if main_path.exists():
        try:
            main_data = json.loads(main_path.read_text(encoding="utf-8"))
        except Exception as e:  # noqa
            log(f"读取 {main_path.name} 失败：{e}")
    if board_path.exists():
        try:
            board_data = json.loads(board_path.read_text(encoding="utf-8"))
        except Exception as e:  # noqa
            log(f"读取 {board_path.name} 失败：{e}")
    return main_data, board_data


def build_context(main_data, board_data):
    lines = []
    if main_data:
        lines.append("## 当日精选（main.py 多类别 TOP）")
        for it in main_data:
            full, lang, stars, cats, desc, status = _proj_info(it)
            cat_s = "/".join(cats) if cats else "-"
            d = (desc or "")[:90].replace("\n", " ")
            lines.append(f"- **{full}** [{cat_s}] ⭐{stars} ({lang}) — {d} | 实测:{status}")
    if board_data:
        lines.append("\n## 板块深潜（board_workflow，每板 TOP 摘要）")
        boards = board_data.get("boards") if isinstance(board_data, dict) else board_data
        if isinstance(boards, list):
            for b in boards:
                bname = b.get("board") or b.get("slug") or b.get("name") or "?"
                items = b.get("results") or b.get("projects") or (
                    [b] if isinstance(b, dict) and b.get("project") else [])
                top = items[:3]
                if not top and isinstance(b, dict) and b.get("project"):
                    top = [b]
                sub = []
                for it in top:
                    full, lang, stars, cats, desc, status = _proj_info(it)
                    sub.append(f"{full}(⭐{stars})")
                lines.append(f"- **{bname}**: {', '.join(sub) if sub else '(无)'}")
    return "\n".join(lines)


def load_history(max_chars=3500):
    if not LINK_INDEX.exists():
        return ""
    txt = LINK_INDEX.read_text(encoding="utf-8")
    if len(txt) > max_chars:
        txt = "...(更早的历史已截断)...\n" + txt[-max_chars:]
    return txt


# ----------------------------------------------------------------------------
# RAG 向量库（Milvus Lite + nomic-embed-text via Ollama）
# ----------------------------------------------------------------------------
def _rag_available():
    return os.path.exists(RAG_VENV_PY)


def rag_retrieve(query, top_k=5, min_date=None):
    """调用 rag_query.py 做向量检索，返回 [{source,date,content,distance}]。
    任何失败都返回 []（调用方降级为 load_history）。"""
    if not query or not query.strip() or not _rag_available():
        return []
    cmd = [
        RAG_VENV_PY,
        os.path.join(RAG_SCRIPT_DIR, "rag_query.py"),
        "--query", query[:1500],
        "--top-k", str(top_k),
    ]
    if min_date:
        cmd += ["--min-date", min_date]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        data = json.loads(proc.stdout)
        if isinstance(data, list):
            return data
    except Exception as e:  # noqa
        log(f"[RAG] 检索失败，降级为 INDEX.md 历史：{e}")
    return []


def rag_ingest():
    """调用 rag_index.py 增量入库（按 source 去重）。best-effort，不阻断主流程。"""
    if not _rag_available():
        return False
    cmd = [RAG_VENV_PY, os.path.join(RAG_SCRIPT_DIR, "rag_index.py")]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        if proc.returncode == 0:
            log("✅ RAG 向量库已增量同步（知识库自进化）")
            return True
        log(f"[RAG] 增量入库返回非零（{proc.returncode}），详见 stderr")
    except Exception as e:  # noqa
        log(f"[RAG] 增量入库失败：{e}")
    return False


# ----------------------------------------------------------------------------
# 模型调用
# ----------------------------------------------------------------------------
def build_daily_messages(context, history):
    system = (
        "你是一位资深开源技术分析师，负责把每日采集的 GitHub 热门项目转化为可行动的知识。"
        "你的职责是「学习」与「链接」：\n"
        "· 学习：提炼今日关键技术主题、新颖点、值得跟进的方向；\n"
        "· 链接：发现项目之间的关联（同领域 / 互补 / 竞争 / 可组合），并尽量连接历史知识。\n"
        "输出严谨、具体、中文、结构化的 Markdown，禁止编造不存在的项目或数据。\n"
        "【格式铁律】直接输出 Markdown 正文，以『## 1.』章节开头；"
        "严禁用代码块（```）包裹整段输出；严禁重复书写主标题『# 学习消化报告』；"
        "若数据不足以支撑某节，明确写「数据不足」，不要编造。\n"
        "【图谱友好】第 1 节『今日技术主题』每条用『主题名：一句话』格式，"
        "便于跨日聚类成知识图谱；第 2 节『项目关联网络』每条明确写出关系类型（同领域/互补/竞争/可组合/延续）。"
    )
    user = f"""下面是今日采集到的 GitHub 热门数据（来自自动化工具的真实运行结果）：

{context}

"""
    if history.strip():
        user += f"""下面是历史累积知识库（此前多日的消化结果），请据此做「与历史知识的连接」：

{history}

"""
    user += (
        "请直接以 Markdown 章节输出以下内容（不要加主标题、不要用代码块包裹）：\n"
        "## 1. 今日技术主题（3-5 个，每条『主题名：一句话』）\n"
        "## 2. 项目关联网络（列出 3-6 组关联，标注关系类型，并说明如何连）\n"
        "## 3. 与历史知识的连接（哪些在延续、哪些是新出现、趋势有何变化）\n"
        "## 4. 推荐深入学习（TOP3 项目 + 理由）\n"
        "## 5. 开放问题 / 值得关注的风险\n"
        "若当日数据不足以支撑某章节，请明确写「数据不足」，不要编造。"
    )
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]


def build_weekly_messages(digests):
    system = (
        "你是一位资深开源技术知识图谱构建者。给定最近若干天「每日技术主题 + 项目关联网络」的摘录，"
        "请产出两份结构化成果（中文 Markdown，禁止编造不存在的项目或数据）：\n\n"
        "## 主题图谱（知识图谱视图）\n"
        "- 把分散在多日的主题聚类为 5-8 个稳定「主题节点」，每个节点给出：\n"
        "  · 出现天数（在窗口内出现几天）\n"
        "  · 趋势：↑上升 / →稳定 / ↓消退\n"
        "  · 关联边：与哪些主题或项目相连，关系类型（同领域/互补/竞争/可组合/延续）\n"
        "  · 涉及日期：列出具体日期\n"
        "- 用「节点—边—节点」的方式呈现，使其像知识图谱而非平铺列表。\n\n"
        "## 本周趋势聚合（起始 ~ 结束）\n"
        "- 上升主题（为什么在升温）\n"
        "- 稳定主线（持续在榜的方向）\n"
        "- 新出现信号（首次出现的主题 / 项目）\n"
        "- 消退 / 风险（热度下降或需警惕的）\n"
        "- 一句话本周结论\n\n"
        "【格式铁律】直接输出上述两个『## 』章节，不要主标题、不要用代码块包裹、不要重复写标题；"
        "若某主题证据不足，明确写「数据不足」。"
    )
    excerpts = []
    for d, t in digests:  # digests 顺序：最新在最前（i=0 为今日）
        excerpts.append(f"【{d.isoformat()}】\n{_extract_theme_network(t)}")
    start = digests[-1][0].isoformat()
    end = digests[0][0].isoformat()
    user = (
        f"以下是 {start} ~ {end} 共 {len(digests)} 天的「每日技术主题 + 项目关联网络」摘录"
        f"（按日期倒序，最新在最前）：\n\n" + "\n\n".join(excerpts) +
        f"\n\n请严格按『## 主题图谱（知识图谱视图）』与『## 本周趋势聚合（{start} ~ {end}）』"
        f"两个章节输出（不要主标题、不要代码块包裹）。"
    )
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]


def _extract_theme_network(text):
    """抽取每日报告的第 1 节（主题）+ 第 2 节（关联网络），截到第 3 节之前，供图谱聚合使用。"""
    m = re.search(r"##\s*1\.(.*?)(?=##\s*3\.)", text, re.DOTALL)
    if m:
        return m.group(1).strip()
    return text[:1600].strip()


def call_ollama(messages, weekly=False):
    payload = {
        "model": MODEL,
        "messages": messages,
        "stream": False,
        "options": {
            "num_predict": int(os.environ.get("LEARN_NUM_PREDICT", "2500" if not weekly else "2000")),
            "num_ctx": int(os.environ.get("LEARN_NUM_CTX", "8192" if not weekly else "16384")),
            "temperature": 0.3,
        },
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        OLLAMA_CHAT,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
            obj = json.loads(resp.read().decode("utf-8"))
        return obj.get("message", {}).get("content", "")
    except Exception as e:  # noqa
        log(f"调用 Ollama 失败：{e}")
        return None


def strip_think(text):
    if not text:
        return ""
    return re.sub(r"<thinking>.*?</think>", "", text, flags=re.DOTALL).strip()


# ----------------------------------------------------------------------------
# 落盘：每日摘要 / 图谱 / 索引
# ----------------------------------------------------------------------------
def save_digest(date, text):
    LEARN_DIR.mkdir(parents=True, exist_ok=True)
    path = LEARN_DIR / f"{date.isoformat()}.md"
    header = (
        f"# 学习消化报告 — {date.isoformat()}\n\n"
        f"> 由 Ollama `{MODEL}` 基于当日真实采集数据生成；工具采集为模型的左膀右臂。\n\n"
    )
    path.write_text(header + text + "\n", encoding="utf-8")
    return path


def _make_one_line_summary(text):
    m = re.search(r"##\s*1\..*?\n(.*?)(?:\n|$)", text, re.DOTALL)
    line = (m.group(1).strip() if m else text.strip().splitlines()[0] if text.strip() else "")
    line = re.sub(r"\s+", " ", line)
    return line[:160]


def load_summaries():
    if SUMMARY_JSON.exists():
        try:
            return json.loads(SUMMARY_JSON.read_text(encoding="utf-8"))
        except Exception:  # noqa
            return {}
    return {}


def save_summary(date, text):
    summaries = load_summaries()
    summaries[date.isoformat()] = _make_one_line_summary(text)
    SUMMARY_JSON.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY_JSON.write_text(
        json.dumps(summaries, ensure_ascii=False, indent=2), encoding="utf-8")


def seed_summaries():
    """把已有每日报告补进 summaries.json（首跑或新增历史日时保证每日摘要完整）。"""
    summaries = load_summaries()
    changed = False
    for p in sorted(LEARN_DIR.glob("20[0-9][0-9]-[0-9][0-9]-[0-9][0-9].md")):
        d = p.stem
        if d not in summaries:
            summaries[d] = _make_one_line_summary(p.read_text(encoding="utf-8"))
            changed = True
    if changed:
        SUMMARY_JSON.parent.mkdir(parents=True, exist_ok=True)
        SUMMARY_JSON.write_text(
            json.dumps(summaries, ensure_ascii=False, indent=2), encoding="utf-8")


def save_weekly(text):
    LINK_DIR.mkdir(parents=True, exist_ok=True)
    WEEKLY_MD.write_text(text + "\n", encoding="utf-8")
    return WEEKLY_MD


def build_index(weekly_text):
    """重组 INDEX.md：图谱优先 + 本周趋势 + 每日摘要（按日期幂等）。"""
    LINK_DIR.mkdir(parents=True, exist_ok=True)
    header = (
        "# 累积知识库（左膀右臂记忆）\n\n"
        "> 知识图谱视图 + 本周趋势由模型每日滚动聚合（近 7 天）；"
        "每日摘要按日期幂等累积于文末。\n"
        "> 完整每日报告见 `reports/learnings/YYYY-MM-DD.md`。\n\n"
    )
    weekly_text = weekly_text or "_本周趋势聚合暂不可用（模型不可用或可用天数不足）。_"
    body = weekly_text.rstrip() + "\n\n---\n\n## 每日摘要\n\n"
    summaries = load_summaries()
    for d in sorted(summaries):
        body += f"### {d}\n- {summaries[d]}\n- 🔗 详情：reports/learnings/{d}.md\n\n"
    LINK_INDEX.write_text(header + body, encoding="utf-8")


def rebuild_index(weekly_text=None):
    if not weekly_text and WEEKLY_MD.exists():
        weekly_text = WEEKLY_MD.read_text(encoding="utf-8")
    build_index(weekly_text)


def collect_week_digests(end_date, days=WEEK_DAYS):
    out = []
    for i in range(days):
        d = end_date - datetime.timedelta(days=i)
        p = LEARN_DIR / f"{d.isoformat()}.md"
        if p.exists():
            out.append((d, p.read_text(encoding="utf-8")))
    return out


# ----------------------------------------------------------------------------
# 主流程
# ----------------------------------------------------------------------------
def main():
    date = datetime.date.today()
    if len(sys.argv) > 1:
        try:
            date = datetime.date.fromisoformat(sys.argv[1])
        except Exception:  # noqa
            pass
    log(f"开始学习+链接+图谱：{date.isoformat()}（模型={MODEL}）")

    main_data, board_data = load_day(date)
    if not main_data and not board_data:
        log("当日无 metadata（main/boards 均未产出），跳过。")
        seed_summaries()
        rebuild_index()
        rag_ingest()
        return 0

    context = build_context(main_data, board_data)
    history = load_history()
    # 用 RAG 向量检索替换「截断的 INDEX.md 历史」，让模型拿到更相关的历史知识
    try:
        rag_hits = rag_retrieve(
            context[:1500], top_k=5,
            min_date=(date - datetime.timedelta(days=45)).isoformat(),
        )
        if rag_hits:
            blocks = []
            for h in rag_hits:
                src = h.get("source", "")
                d = h.get("date", "")
                c = (h.get("content") or "")[:600].replace("\n", " ")
                blocks.append(f"- （{d} · {src}）{c}")
            history = "## 相关历史知识（RAG 向量检索，按相似度排序）\n" + "\n".join(blocks)
            log(f"✅ RAG 检索到 {len(rag_hits)} 条相关历史，已注入上下文（替代截断的 INDEX.md）")
    except Exception as e:  # noqa
        log(f"[RAG] 上下文注入跳过，沿用 INDEX.md 历史：{e}")
    messages = build_daily_messages(context, history)

    content = call_ollama(messages)
    if not content:
        log("⚠️ Ollama/DeepSeek 不可用，跳过学习步骤（不影响主流程）。")
        seed_summaries()
        rebuild_index()
        rag_ingest()
        return 0

    clean = strip_think(content) or content
    save_digest(date, clean)
    save_summary(date, clean)
    log(f"✅ 每日消化报告：{LEARN_DIR / (date.isoformat() + '.md')}")

    # 滚动 7 天「主题图谱 + 本周趋势聚合」
    digests = collect_week_digests(date)
    weekly_text = None
    if len(digests) >= 2:
        w_msgs = build_weekly_messages(digests)
        w_content = call_ollama(w_msgs, weekly=True)
        if w_content:
            weekly_text = strip_think(w_content) or w_content
            save_weekly(weekly_text)
            log("✅ 本周主题图谱 + 趋势聚合已更新")
        else:
            log("⚠️ 本周聚合模型调用失败，沿用上一份图谱（如有）")
    else:
        log(f"本周可用天数={len(digests)} < 2，跳过聚合，仅更新每日摘要")

    seed_summaries()
    rebuild_index(weekly_text)
    log("✅ INDEX.md 已重组为知识图谱优先视图")
    rag_ingest()
    return 0


if __name__ == "__main__":
    sys.exit(main())
