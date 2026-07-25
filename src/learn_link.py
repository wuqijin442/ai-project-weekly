#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""learn_link.py — 用 Ollama 上的 deepseek-r1:32b 对当日 GitHub 热门做「学习 + 链接」。

读取当日 metadata（main.py 的每日多类别 + board_workflow 的板块深潜），
结合历史知识库（knowledge-base/learn_links/INDEX.md），让模型：
  1) 学习：提炼今日技术主题、新颖点、值得跟进的方向；
  2) 链接：发现项目间关联（同领域/互补/竞争/可组合），并连接历史知识；
产出结构化「学习消化报告」reports/learnings/YYYY-MM-DD.md，
并把核心洞察沉淀到累积知识库（让这些采集工具成为模型的左膀右臂）。

实现：仅依赖 Python 标准库（urllib 调 Ollama HTTP API），Ollama 不可用时优雅跳过，
不阻断整个自动化。
"""
import os
import sys
import json
import re
import datetime
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
META_DIR = ROOT / "data" / "metadata"
LEARN_DIR = ROOT / "reports" / "learnings"
LINK_INDEX = ROOT / "knowledge-base" / "learn_links" / "INDEX.md"

OLLAMA_CHAT = "http://localhost:11434/api/chat"
MODEL = os.environ.get("LEARN_MODEL", "deepseek-r1:32b")
HTTP_TIMEOUT = int(os.environ.get("LEARN_TIMEOUT", "600"))


def log(msg):
    ts = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[learn_link {ts}] {msg}", flush=True)


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
        # board_data 可能是 {boards:[...]} 或 [...]；尽量适配
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


def build_messages(context, history):
    system = (
        "你是一位资深开源技术分析师，负责把每日采集的 GitHub 热门项目转化为可行动的知识。"
        "你的职责是「学习」与「链接」：\n"
        "· 学习：提炼今日关键技术主题、新颖点、值得跟进的方向；\n"
        "· 链接：发现项目之间的关联（同领域 / 互补 / 竞争 / 可组合），并尽量连接历史知识。\n"
        "输出严谨、具体、中文、结构化的 Markdown，禁止编造不存在的项目或数据。\n"
        "【格式铁律】直接输出 Markdown 正文，以『## 1.』章节开头；"
        "严禁用代码块（```）包裹整段输出；严禁重复书写主标题『# 学习消化报告』；"
        "若数据不足以支撑某节，明确写「数据不足」，不要编造。"
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
        "## 1. 今日技术主题（3-5 个，每条一句话）\n"
        "## 2. 项目关联网络（列出 3-6 组关联：同领域/互补/竞争/可组合，并说明如何连）\n"
        "## 3. 与历史知识的连接（哪些在延续、哪些是新出现、趋势有何变化）\n"
        "## 4. 推荐深入学习（TOP3 项目 + 理由）\n"
        "## 5. 开放问题 / 值得关注的风险\n"
        "若当日数据不足以支撑某章节，请明确写「数据不足」，不要编造。"
    )
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]


def call_ollama(messages):
    payload = {
        "model": MODEL,
        "messages": messages,
        "stream": False,
        "options": {
            "num_predict": int(os.environ.get("LEARN_NUM_PREDICT", "2500")),
            "num_ctx": int(os.environ.get("LEARN_NUM_CTX", "8192")),
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


def save_digest(date, text):
    LEARN_DIR.mkdir(parents=True, exist_ok=True)
    path = LEARN_DIR / f"{date.isoformat()}.md"
    header = (
        f"# 学习消化报告 — {date.isoformat()}\n\n"
        f"> 由 Ollama `{MODEL}` 基于当日真实采集数据生成；工具采集为模型的左膀右臂。\n\n"
    )
    path.write_text(header + text + "\n", encoding="utf-8")
    return path


def append_index(date, text):
    LINK_INDEX.parent.mkdir(parents=True, exist_ok=True)
    summary = text.replace("\n", " ").strip()
    summary = summary[:200] + ("…" if len(text) > 200 else "")
    block = f"\n## {date.isoformat()}\n- {summary}\n- 🔗 详情：reports/learnings/{date.isoformat()}.md\n"
    if not LINK_INDEX.exists():
        LINK_INDEX.write_text(
            "# 累积知识库（左膀右臂记忆）\n\n"
            "本文件由 learn_link.py 每日追加，沉淀 GitHub 热门的「学习 + 链接」洞察，"
            "供模型跨日连接知识。\n" + block, encoding="utf-8")
    else:
        with LINK_INDEX.open("a", encoding="utf-8") as f:
            f.write(block)


def main():
    date = datetime.date.today()
    if len(sys.argv) > 1:
        try:
            date = datetime.date.fromisoformat(sys.argv[1])
        except Exception:  # noqa
            pass
    log(f"开始学习+链接：{date.isoformat()}")

    main_data, board_data = load_day(date)
    if not main_data and not board_data:
        log("当日无 metadata（main/boards 均未产出），跳过。")
        return 0

    context = build_context(main_data, board_data)
    history = load_history()
    messages = build_messages(context, history)

    content = call_ollama(messages)
    if not content:
        log("⚠️ Ollama/DeepSeek 不可用，跳过学习步骤（不影响主流程）。")
        return 0

    clean = strip_think(content) or content
    path = save_digest(date, clean)
    append_index(date, clean)
    log(f"✅ 学习消化报告已生成：{path}")
    log(f"✅ 累积知识库已更新：{LINK_INDEX}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
