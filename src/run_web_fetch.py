# -*- coding: utf-8 -*-
"""
WebFetch 驱动的每日归档入口（修正版）。

背景 / 根因（2026-08-19）：
- github.com/trending 主站被 IP 层阻断（urllib 空 body），curl 亦不可达。
- 官方 API 备用通道（main.fetch_trending_via_api）按「近期有推送+star≥200 按 star 降序」
  返回的是 awesome / public-apis / freeCodeCamp 等常年大库，≠ 当日飙升榜，
  直接用于 Vibe Coding 筛选会严重误判（见 2026-08-19 验证：Top5 误成 awesome/public-apis）。
- 唯一可用的真实飙升榜来源是 WebFetch 代理通道，但模型输出截断，**稳定只返回前 ~13 条**
  （要求「14–25 名」仍从顶部取）。下半段不可达是环境限制，非代码 bug。

因此正确策略（本文件）：
- agent 用 WebFetch 抓当日真实飙升榜（可达前 ~13 条，带真实「stars today」），
  转写为 JSON（owner/name/description/language/stars/today_growth）落到
  ima_carrier/.trending_<date>.json；
- 本驱动读取该 JSON，复用 github_archive 的 enrich_with_api → vibe_filter →
  build_obsidian → build_ima_carrier → git_sync_obsidian（win 分支），
  全程规范化、不手工 patch；
- 可达条目上限 ~13 条，对 Vibe Coding 筛选足够（爆款必在头部），
  「全赛道爆款」按可达条目输出并诚实标注「部分」。

用法：
  python src/run_web_fetch.py --date 2026-08-19
  python src/run_web_fetch.py --date 2026-08-19 --no-git   # 仅本地生成审查
  python src/run_web_fetch.py --date 2026-08-19 --data path/to/trending.json
"""
import sys
import os
import json
import argparse
import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import github_archive as ga  # noqa: E402


def load_trending(date, data_path=None):
    if data_path is None:
        data_path = ga.IMA_CARRIER / f".trending_{date.isoformat()}.json"
    data_path = Path(data_path)
    if not data_path.exists():
        ga.log(f"❌ 未找到趋势 JSON：{data_path}（请先由 WebFetch 生成）")
        sys.exit(2)
    raw = json.loads(data_path.read_text(encoding="utf-8"))
    ga.log(f"载入趋势 JSON：{len(raw)} 个仓库（{data_path.name}）")
    projects = []
    for it in raw:
        owner = it["owner"].strip()
        name = it["name"].strip()
        full = f"{owner}/{name}"
        projects.append({
            "owner": owner, "name": name, "full": full,
            "url": it.get("url") or f"https://github.com/{full}",
            "description": it.get("description", "") or "",
            "language": it.get("language", "Unknown") or "Unknown",
            "today_growth": int(it.get("today_growth", 0) or 0),
            "growth_period": "today",
            "stars": int(it.get("stars", 0) or 0),
            "forks": int(it.get("forks", 0) or 0),
            "topics": it.get("topics", []) or [],
            "license": it.get("license", "NOASSERTION") or "NOASSERTION",
            "created_at": it.get("created_at", "") or "",
            "source": "trending-webfetch",
        })
    return projects


def main():
    ap = argparse.ArgumentParser(description="WebFetch 驱动的 GitHub AI 项目每日归档")
    ap.add_argument("--date", default=datetime.date.today().isoformat(),
                    help="归档日期 YYYY-MM-DD（默认今天）")
    ap.add_argument("--no-git", action="store_true",
                    help="仅本地生成 Obsidian + ima 载体，不提交/不推送")
    ap.add_argument("--data", default=None,
                    help="趋势 JSON 路径（默认 ima_carrier/.trending_<date>.json）")
    args = ap.parse_args()

    date = datetime.date.fromisoformat(args.date)
    ga.ensure_token_env()
    ga.log(f"=== WebFetch 归档启动 {date.isoformat()} ===")

    projects = load_trending(date, args.data)
    ga.enrich_with_api(projects)
    top, meta = ga.vibe_filter(projects, date)
    if not top:
        ga.log("❌ 筛选后无入选项目，终止")
        sys.exit(2)
    ga.log(f"入选 Top{len(top)}：{', '.join(p['full'] for p in top)}")

    ga.build_obsidian(date, top, projects)
    carrier = ga.build_ima_carrier(date, top, projects)
    ga.log(f"ima 载体：{carrier}")

    if args.no_git:
        ga.log("⏭️ --no-git：跳过提交/推送（仅本地生成，待审查）")
        return

    ok, info = ga.git_sync_obsidian(date, do_push=True)
    ga.log(f"git 同步 {'✅ OK' if ok else '⚠️ FAIL'}：{str(info)[:160]}")
    if not ok:
        ga.log("提示：推送失败已写 Logs/PUSH_STUCK.flag，网络恢复后重跑本命令即可补推")
        sys.exit(3)
    ga.log("=== 归档完成 ===")


if __name__ == "__main__":
    main()
