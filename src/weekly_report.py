#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
周报生成器 — reports/weekly/Weekly-Top10.md

聚合本周（周一~周日）已有的真实产物：
  - data/metadata/YYYY-MM-DD.json        （步骤1 每日多类别日报的真实运行结果）
  - data/metadata/YYYY-MM-DD-boards.json （步骤2 11 板块深潜的真实运行结果）

真实运行铁律：本脚本**不做任何网络抓取、不推测**，只对已落盘的真实 Clone/安装/冒烟结果
做统计与排序。缺失的日期如实标注为"无数据"。

排序口径（Weekly TOP10）：
  1) 本周上榜天数（出现在每日 TOP 榜的次数）降序
  2) 真实落地得分（安装成功 +2 / 冒烟成功 +3）降序
  3) Star 降序

用法：
  python src/weekly_report.py                # 以今天所在自然周生成
  python src/weekly_report.py --date 2026-08-09
  python src/weekly_report.py --no-push      # 只生成不提交
"""
import os
import sys
import json
import argparse
import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import main as _main  # noqa
from main import log, sync_to_github, pre_sync_pull  # noqa

ROOT = Path(__file__).resolve().parent.parent
META = ROOT / "data" / "metadata"
WEEKLY = ROOT / "reports" / "weekly"


def week_range(day: datetime.date):
    """返回该日期所在自然周的周一~周日日期列表。"""
    monday = day - datetime.timedelta(days=day.weekday())
    return [monday + datetime.timedelta(days=i) for i in range(7)]


def load_daily(day: datetime.date):
    p = META / f"{day.isoformat()}.json"
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:  # noqa
        log(f"⚠️ 解析失败 {p.name}: {e}")
        return None


def load_boards(day: datetime.date):
    p = META / f"{day.isoformat()}-boards.json"
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:  # noqa
        log(f"⚠️ 解析失败 {p.name}: {e}")
        return None


def land_score(rec):
    """真实落地得分：只认真实执行结果。"""
    s = 0
    if rec.get("install") == "success":
        s += 2
    if rec.get("run") == "success":
        s += 3
    if rec.get("clone"):
        s += 1
    return s


def collect(days):
    """聚合每日 TOP 榜项目。返回 (agg, daily_stats)"""
    agg = {}
    daily_stats = []
    for d in days:
        items = load_daily(d)
        if not items:
            daily_stats.append({"date": d, "ok": False})
            continue
        st = {"date": d, "ok": True, "total": len(items),
              "clone": 0, "install": 0, "run": 0, "langs": {}, "cats": {}}
        for rec in items:
            proj = rec.get("project", {})
            full = proj.get("full")
            if not full:
                continue
            if rec.get("clone"):
                st["clone"] += 1
            if rec.get("install") == "success":
                st["install"] += 1
            if rec.get("run") == "success":
                st["run"] += 1
            lang = proj.get("language") or "Unknown"
            st["langs"][lang] = st["langs"].get(lang, 0) + 1
            for c in proj.get("categories") or []:
                st["cats"][c] = st["cats"].get(c, 0) + 1

            e = agg.setdefault(full, {
                "full": full, "url": proj.get("url", ""),
                "language": lang, "desc": proj.get("description", ""),
                "stars": 0, "days": [], "categories": set(),
                "best_land": 0, "install_ok": 0, "run_ok": 0,
                "clone_ok": 0, "appear": 0, "score": 0,
            })
            e["appear"] += 1
            e["days"].append(d.strftime("%m-%d"))
            e["stars"] = max(e["stars"], int(proj.get("stars") or 0))
            e["categories"].update(proj.get("categories") or [])
            e["best_land"] = max(e["best_land"], land_score(rec))
            e["score"] = max(e["score"], float(rec.get("score") or 0))
            if rec.get("clone"):
                e["clone_ok"] += 1
            if rec.get("install") == "success":
                e["install_ok"] += 1
            if rec.get("run") == "success":
                e["run_ok"] += 1
            if not e["desc"]:
                e["desc"] = proj.get("description", "")
        daily_stats.append(st)
    return agg, daily_stats


def collect_boards(days):
    """聚合板块深潜结果：按板块统计 clone/install/run，并挑出真实冒烟成功的项目。"""
    board_stat = {}
    smoke_ok = {}
    covered = []
    for d in days:
        data = load_boards(d)
        if not data:
            continue
        covered.append(d)
        for board, payload in data.items():
            # 元数据结构：{board: {"label": 中文名, "top": [...], "results": [测试记录]}}
            if isinstance(payload, dict):
                items = payload.get("results") or []
                label = payload.get("label")
            else:
                items = payload or []
                label = None
            b = board_stat.setdefault(board, {"tested": 0, "clone": 0, "install": 0,
                                              "run": 0, "label": label})
            if label and not b.get("label"):
                b["label"] = label
            for rec in items:
                if not isinstance(rec, dict):
                    continue
                b["tested"] += 1
                if rec.get("clone"):
                    b["clone"] += 1
                if rec.get("install") == "success":
                    b["install"] += 1
                if rec.get("run") == "success":
                    b["run"] += 1
                    proj = rec.get("project", {})
                    full = proj.get("full")
                    if full:
                        s = smoke_ok.setdefault(full, {
                            "full": full, "url": proj.get("url", ""),
                            "language": proj.get("language") or "Unknown",
                            "stars": int(proj.get("stars") or 0),
                            "boards": set(), "dates": set(),
                            "score": float(rec.get("score") or 0),
                        })
                        s["boards"].add(board)
                        s["dates"].add(d.strftime("%m-%d"))
                        s["stars"] = max(s["stars"], int(proj.get("stars") or 0))
                        s["score"] = max(s["score"], float(rec.get("score") or 0))
    return board_stat, smoke_ok, covered


BOARD_CN = {
    "large-language-models": "大语言模型",
    "artificial-intelligence": "人工智能",
    "rag": "检索增强生成 RAG",
    "stable-diffusion": "扩散模型",
    "computer-vision": "计算机视觉",
    "speech-recognition": "语音识别",
    "robotics": "机器人",
    "mlops": "MLOps",
    "vector-database": "向量数据库",
    "prompt-engineering": "提示工程",
    "fine-tuning": "微调",
}


def render(day, days, agg, daily_stats, board_stat, smoke_ok, boards_days):
    monday, sunday = days[0], days[-1]
    iso_year, iso_week, _ = day.isocalendar()

    ranked = sorted(
        agg.values(),
        key=lambda e: (e["appear"], e["best_land"], e["stars"]),
        reverse=True,
    )[:10]

    have = [s for s in daily_stats if s.get("ok")]
    miss = [s for s in daily_stats if not s.get("ok")]

    L = []
    L.append(f"# GitHub 开源项目周报 — {iso_year}-W{iso_week:02d}"
             f"（{monday.isoformat()} ~ {sunday.isoformat()}）")
    L.append("")
    L.append("> 本周报**不做任何新的网络抓取**，只聚合本周已落盘的真实 Clone/安装/冒烟运行结果；"
             "缺失日期如实标注，未运行项不计入成功数。")
    L.append("")
    L.append(f"**统计口径**：自然周（周一~周日）　**有数据天数**：{len(have)}/7　"
             f"**板块深潜覆盖天数**：{len(boards_days)}/7")
    if miss:
        L.append("")
        L.append("**⚠️ 无数据日期**：" + "、".join(s["date"].isoformat() for s in miss)
                 + "（当日 Windows 端未产出，非本周报遗漏）")
    L.append("")

    # ---- 本周汇总 ----
    tot_t = sum(s["total"] for s in have)
    tot_c = sum(s["clone"] for s in have)
    tot_i = sum(s["install"] for s in have)
    tot_r = sum(s["run"] for s in have)
    bt = sum(b["tested"] for b in board_stat.values())
    bc = sum(b["clone"] for b in board_stat.values())
    bi = sum(b["install"] for b in board_stat.values())
    br = sum(b["run"] for b in board_stat.values())

    L.append("## 一、本周真实执行汇总")
    L.append("")
    L.append("| 来源 | 测试项目 | Clone 成功 | 安装成功 | 冒烟运行成功 |")
    L.append("|---|---|---|---|---|")
    L.append(f"| 每日多类别榜（步骤1） | {tot_t} | {tot_c} | {tot_i} | {tot_r} |")
    L.append(f"| 11 板块深潜（步骤2） | {bt} | {bc} | {bi} | {br} |")
    L.append(f"| **合计** | **{tot_t + bt}** | **{tot_c + bc}** | **{tot_i + bi}** | **{tot_r + br}** |")
    L.append("")

    # ---- 每日明细 ----
    L.append("### 每日明细（步骤1）")
    L.append("")
    L.append("| 日期 | 上榜项目 | Clone | 安装成功 | 冒烟成功 |")
    L.append("|---|---|---|---|---|")
    for s in daily_stats:
        if s.get("ok"):
            L.append(f"| {s['date'].isoformat()} | {s['total']} | {s['clone']} | "
                     f"{s['install']} | {s['run']} |")
        else:
            L.append(f"| {s['date'].isoformat()} | — | — | — | — |")
    L.append("")

    # ---- TOP10 ----
    L.append("## 二、本周 TOP10（按上榜天数 → 真实落地 → Star 排序）")
    L.append("")
    if not ranked:
        L.append("_本周无可用日报数据，无法生成 TOP10。_")
    else:
        L.append("| # | 项目 | 语言 | Star | 上榜天数 | 真实落地 | 类别 |")
        L.append("|---|---|---|---|---|---|---|")
        for i, e in enumerate(ranked, 1):
            land = []
            if e["install_ok"]:
                land.append(f"安装✅×{e['install_ok']}")
            if e["run_ok"]:
                land.append(f"冒烟✅×{e['run_ok']}")
            if not land:
                land.append("仅 Clone")
            cats = "、".join(sorted(e["categories"])) or "—"
            L.append(f"| {i} | [{e['full']}]({e['url']}) | {e['language']} | "
                     f"{e['stars']:,} | {e['appear']}（{'/'.join(e['days'])}） | "
                     f"{'，'.join(land)} | {cats} |")
        L.append("")
        L.append("### TOP10 逐项说明")
        L.append("")
        for i, e in enumerate(ranked, 1):
            L.append(f"**{i}. {e['full']}**　`{e['language']}`　★{e['stars']:,}")
            L.append("")
            L.append(f"- 地址：{e['url']}")
            if e["desc"]:
                L.append(f"- 简介：{e['desc']}")
            L.append(f"- 本周上榜：{e['appear']} 天（{'、'.join(e['days'])}）")
            L.append(f"- 真实执行：Clone 成功 {e['clone_ok']} 次 / 安装成功 "
                     f"{e['install_ok']} 次 / 冒烟运行成功 {e['run_ok']} 次")
            L.append(f"- 本周最高 AI 评分：{e['score']:.0f}/100")
            L.append("")

    # ---- 板块 ----
    L.append("## 三、11 板块深潜本周聚合")
    L.append("")
    if not board_stat:
        L.append("_本周无板块深潜数据。_")
    else:
        L.append("| 板块 | 测试 | Clone | 安装成功 | 冒烟成功 | 安装成功率 |")
        L.append("|---|---|---|---|---|---|")
        for b, v in sorted(board_stat.items(), key=lambda kv: -kv[1]["install"]):
            rate = (v["install"] / v["tested"] * 100) if v["tested"] else 0
            L.append(f"| {v.get('label') or BOARD_CN.get(b, b)} | {v['tested']} | {v['clone']} | "
                     f"{v['install']} | {v['run']} | {rate:.0f}% |")
        L.append("")

    # ---- 冒烟成功名单（最硬的真实结果）----
    L.append("## 四、本周真实冒烟运行成功名单（板块深潜）")
    L.append("")
    if not smoke_ok:
        L.append("_本周板块深潜无冒烟运行成功项目。_")
    else:
        L.append("| 项目 | 语言 | Star | 所属板块 | 成功日期 | 评分 |")
        L.append("|---|---|---|---|---|---|")
        for s in sorted(smoke_ok.values(), key=lambda x: -x["stars"]):
            L.append(f"| [{s['full']}]({s['url']}) | {s['language']} | {s['stars']:,} | "
                     f"{'、'.join(BOARD_CN.get(b, b) for b in sorted(s['boards']))} | "
                     f"{'、'.join(sorted(s['dates']))} | {s['score']:.0f} |")
        L.append("")

    # ---- 趋势观察 ----
    langs, cats = {}, {}
    for e in agg.values():
        langs[e["language"]] = langs.get(e["language"], 0) + e["appear"]
        for c in e["categories"]:
            cats[c] = cats.get(c, 0) + e["appear"]
    L.append("## 五、本周趋势观察（基于真实落地项目）")
    L.append("")
    if langs:
        L.append("- **语言分布**（按上榜人次）：" + "，".join(
            f"{k}×{v}" for k, v in sorted(langs.items(), key=lambda kv: -kv[1])))
    if cats:
        L.append("- **类别分布**（按上榜人次）：" + "，".join(
            f"{k}×{v}" for k, v in sorted(cats.items(), key=lambda kv: -kv[1])))
    if tot_t:
        L.append(f"- **落地难度**：步骤1 榜单项目安装成功率 {tot_i / tot_t * 100:.0f}%"
                 f"（{tot_i}/{tot_t}），冒烟运行成功率 {tot_r / tot_t * 100:.0f}%"
                 f"（{tot_r}/{tot_t}）——大量热门仓库为文档/教程/大型工程，无法一键安装即跑。")
    if bt:
        L.append(f"- **板块深潜落地率**：安装成功率 {bi / bt * 100:.0f}%（{bi}/{bt}），"
                 f"冒烟成功率 {br / bt * 100:.0f}%（{br}/{bt}）。")
    L.append("")
    L.append("---")
    L.append("")
    L.append(f"_生成时间：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}　"
             f"数据源：data/metadata/ 本周真实运行产物_")
    L.append("")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", help="YYYY-MM-DD，默认今天")
    ap.add_argument("--no-push", action="store_true")
    args = ap.parse_args()

    day = (datetime.date.fromisoformat(args.date) if args.date
           else datetime.date.today())
    days = week_range(day)
    log(f"=== 周报生成 {days[0]} ~ {days[-1]} ===")

    if not args.no_push:
        pre_sync_pull()

    agg, daily_stats = collect(days)
    board_stat, smoke_ok, boards_days = collect_boards(days)
    log(f"聚合完成：日报可用 {sum(1 for s in daily_stats if s.get('ok'))}/7 天，"
        f"板块可用 {len(boards_days)}/7 天，去重项目 {len(agg)} 个")

    WEEKLY.mkdir(parents=True, exist_ok=True)
    out = WEEKLY / "Weekly-Top10.md"
    text = render(day, days, agg, daily_stats, board_stat, smoke_ok, boards_days)
    out.write_text(text, encoding="utf-8")
    log(f"周报已生成：{out}")

    # 同时留一份带周次的归档，避免下周覆盖后无法回溯
    iso_year, iso_week, _ = day.isocalendar()
    arch = WEEKLY / f"Weekly-{iso_year}-W{iso_week:02d}.md"
    arch.write_text(text, encoding="utf-8")
    log(f"周报归档：{arch}")

    if args.no_push:
        log("--no-push：跳过提交推送")
        return 0

    ok, err = sync_to_github(day)
    if ok:
        log("✅ 周报已推送")
    else:
        log(f"❌ 周报推送失败：{err}")
    log("=== 周报完成 ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
