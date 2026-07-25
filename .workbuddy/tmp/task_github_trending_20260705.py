#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub AI 项目自动归档任务
- 工作日：Vibe Coding 赛道日报 Top 5
- 周末：全赛道 AI 周报 Top 10
"""
import os
import re
import sys
import json
import logging
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import quote

WORKSPACE = Path("D:/Users/Administrator/Desktop/AI Project Weekly")
VAULT = WORKSPACE / "Obsidian_Vault"
LOGS = WORKSPACE / "logs"
TMP = WORKSPACE / ".workbuddy" / "tmp"

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

VIBE_KEYWORDS = [
    "cursor", "cline", "aider", "continue", "swe-agent", "open-interpreter",
    "browser-use", "gpt-engineer", "meta-gpt", "devin", "autocode", "copilot",
    "cli-agent", "code-generator", "llm-dev"
]

AI_KEYWORDS = [
    "ai", "artificial intelligence", "artificial-intelligence", "machine learning",
    "machine-learning", "deep learning", "deep-learning", "neural network", "llm",
    "large language model", "agent", "chatbot", "gpt", "claude", "openai", "anthropic",
    "generative", "genai", "multimodal", "rag", "retrieval augmented", "copilot",
    "autocode", "vibe coding", "code assistant", "coding assistant", "mcp", "swe",
    "software engineering", "computer vision", "nlp", "natural language", "vision",
    "diffusion", "transformer", "stable diffusion", "browser-use", "ai agent",
    "video-use", "ai coding", "ai-coding"
]


def setup_logging():
    LOGS.mkdir(exist_ok=True)
    log_file = LOGS / f"task_{datetime.now().strftime('%Y-%m-%d')}.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return log_file


def fetch_trending_page(url):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "DNT": "1",
        "Connection": "keep-alive",
    }
    try:
        resp = requests.get(url, headers=headers, timeout=30)
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        logging.error(f"请求失败 {url}: {e}")
        return None


def parse_trending_repos(html):
    """从 GitHub trending HTML 解析项目列表"""
    soup = BeautifulSoup(html, "html.parser")
    repos = []
    articles = soup.find_all("article", class_="Box-row")
    logging.info(f"HTML 中找到 {len(articles)} 个 article.Box-row")
    for article in articles:
        h2 = article.find("h2")
        if not h2:
            continue
        a = h2.find("a", href=True)
        if not a:
            continue
        href = a.get("href", "").strip()
        if href.startswith("/"):
            href = href[1:]
        full_name = href.replace(" ", "").replace("\n", "")
        if "/" not in full_name:
            continue
        parts = full_name.split("/")
        owner = parts[0]
        repo = parts[1]
        desc_p = article.find("p", class_="col-9")
        description = ""
        if desc_p:
            description = desc_p.get_text(strip=True)
        lang_span = article.find("span", itemprop="programmingLanguage")
        language = lang_span.get_text(strip=True) if lang_span else ""
        stars_text = ""
        # 先尝试精确匹配趋势文本
        for span in article.find_all("span"):
            txt = span.get_text(strip=True)
            if "star" in txt.lower() and ("today" in txt.lower() or "this week" in txt.lower() or "this month" in txt.lower()):
                stars_text = txt
                break
        if not stars_text:
            for div in article.find_all("div"):
                txt = div.get_text(strip=True)
                if "star" in txt.lower() and ("today" in txt.lower() or "this week" in txt.lower() or "this month" in txt.lower()):
                    stars_text = txt
                    break
        repos.append({
            "full_name": full_name,
            "owner": owner,
            "repo": repo,
            "description": description,
            "language": language,
            "stars_text": stars_text,
        })
    return repos


def parse_stars_text(text):
    """解析 '1,234 stars this week' / '2.3k stars this week'"""
    if not text:
        return 0
    text = text.lower().replace(",", "")
    m = re.search(r"([\d.]+)\s*([kmb]?)\s*(?:stars?|starred)", text)
    if not m:
        m = re.search(r"([\d.]+)\s*([kmb]?)", text)
    if not m:
        return 0
    num = float(m.group(1))
    unit = m.group(2)
    multiplier = {"k": 1000, "m": 1000000, "b": 1000000000, "": 1}
    return int(num * multiplier.get(unit, 1))


def fetch_trending_repos(mode):
    """
    获取趋势项目。
    先尝试 /trending/ai?since=weekly/daily；若为空则退回到总榜并过滤。
    """
    since = "weekly" if mode == "weekend" else "daily"
    urls = [
        f"https://github.com/trending/ai?since={since}",
        f"https://github.com/trending?since={since}",
    ]
    all_repos = []
    for url in urls:
        html = fetch_trending_page(url)
        if not html:
            continue
        repos = parse_trending_repos(html)
        if not repos:
            logging.warning(f"{url} 未解析到项目")
            continue
        logging.info(f"从 {url} 解析到 {len(repos)} 个项目")
        if "trending/ai" in url:
            return repos
        # 总榜需要过滤
        all_repos.extend(repos)
    if not all_repos:
        return []
    # 去重（按 full_name）
    seen = set()
    unique = []
    for r in all_repos:
        if r["full_name"] not in seen:
            seen.add(r["full_name"])
            unique.append(r)
    # 过滤 AI 相关
    filtered = []
    for r in unique:
        hay = f"{r['full_name']} {r['description']}".lower()
        if any(k in hay for k in AI_KEYWORDS):
            filtered.append(r)
    if not filtered:
        logging.warning("过滤后无 AI 项目，返回总榜全部项目")
        return unique
    return filtered


def github_headers():
    h = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
    if GITHUB_TOKEN:
        h["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    return h


def get_repo_details(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}"
    try:
        resp = requests.get(url, headers=github_headers(), timeout=30)
        if resp.status_code == 404:
            logging.error(f"仓库不存在: {owner}/{repo}")
            return None
        resp.raise_for_status()
        data = resp.json()
        return {
            "full_name": data.get("full_name", f"{owner}/{repo}"),
            "owner": data.get("owner", {}).get("login", owner),
            "html_url": data.get("html_url", f"https://github.com/{owner}/{repo}"),
            "description": data.get("description") or "",
            "stargazers_count": data.get("stargazers_count", 0),
            "language": data.get("language", ""),
            "topics": data.get("topics", []),
            "created_at": data.get("created_at", ""),
            "updated_at": data.get("updated_at", ""),
            "pushed_at": data.get("pushed_at", ""),
        }
    except Exception as e:
        logging.error(f"获取 {owner}/{repo} 详情失败: {e}")
        return None


def get_readme_summary(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/readme"
    try:
        resp = requests.get(url, headers=github_headers(), timeout=30)
        if resp.status_code in (404, 451):
            return ""
        resp.raise_for_status()
        data = resp.json()
        import base64
        content = base64.b64decode(data.get("content", "")).decode("utf-8", errors="ignore")
        # 提取第一个非空、非标题、非图片/链接的段落
        for line in content.split("\n"):
            line = line.strip()
            if not line:
                continue
            if line.startswith("#"):
                continue
            if line.startswith("!") or line.startswith("["):
                continue
            if line.startswith("<") and line.endswith(">"):
                continue
            # 清理 markdown 链接和粗体
            clean = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", line)
            clean = re.sub(r"[*_`]{1,2}", "", clean)
            if clean:
                return clean[:500]
        return ""
    except Exception as e:
        logging.error(f"获取 {owner}/{repo} README 失败: {e}")
        return ""


def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "_", name)


def generate_obsidian(projects, mode, today, weekday_cn):
    VAULT.mkdir(exist_ok=True)
    (VAULT / "Daily").mkdir(exist_ok=True)
    (VAULT / "Weekly").mkdir(exist_ok=True)
    (VAULT / "Projects").mkdir(exist_ok=True)

    if mode == "weekday":
        index_path = VAULT / "Daily" / f"Vibe-Coding-{today}.md"
        title = f"GitHub Vibe Coding 日报 - {today}"
    else:
        index_path = VAULT / "Weekly" / f"AI-Weekly-{today}.md"
        title = f"GitHub AI 周报 - {today}"

    # 索引文件
    lines = []
    lines.append("---")
    lines.append(f"date: {today}")
    lines.append(f"mode: {mode}")
    lines.append(f"count: {len(projects)}")
    lines.append("tags: [AI, Trending, GitHub]")
    lines.append("---")
    lines.append("")
    lines.append(f"# {title}")
    lines.append("")
    lines.append(f"- 日期：{today}（{weekday_cn}）")
    lines.append(f"- 模式：{'工作日 / Vibe Coding 赛道' if mode == 'weekday' else '周末 / 全赛道 AI'}")
    lines.append(f"- 项目数量：{len(projects)}")
    lines.append("")
    lines.append("| 项目 | 作者 | 新增 Star | 总 Star | 语言 | 简介 |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for p in projects:
        proj_wiki = f"[[{sanitize_filename(p['repo'])}|{p['full_name']}]]"
        desc = p.get("description", "") or ""
        lines.append(
            f"| {proj_wiki} | {p['owner']} | {p.get('weekly_growth', 0)} | "
            f"{p.get('stargazers_count', 0)} | {p.get('language', '')} | {desc} |"
        )
    lines.append("")
    lines.append("## 反向链接")
    lines.append("- 返回全局索引：[[_Index]]")
    lines.append("")
    index_path.write_text("\n".join(lines), encoding="utf-8")

    # 项目详情页
    for p in projects:
        proj_file = VAULT / "Projects" / f"{sanitize_filename(p['repo'])}.md"
        lang = p.get("language", "") or "Unknown"
        tags = ["AI", "Trending"]
        if lang and lang != "Unknown":
            tags.append(lang)

        plines = []
        plines.append("---")
        plines.append(f"aliases: [{p['full_name']}]")
        plines.append(f"tags: [{', '.join(tags)}]")
        plines.append(f"stars: {p.get('stargazers_count', 0)}")
        plines.append(f"weekly_growth: {p.get('weekly_growth', 0)}")
        plines.append("status: 待填写")
        plines.append(f"date_accessed: {today}")
        plines.append("---")
        plines.append("")
        plines.append(f"# {p['full_name']}")
        plines.append("")
        plines.append("## 项目定位")
        summary = p.get("readme_summary", "") or p.get("description", "") or "暂无描述"
        plines.append(summary)
        plines.append("")
        plines.append("## 技术栈")
        plines.append(f"- 主要语言：{lang}")
        if p.get("topics"):
            plines.append(f"- 相关标签：{', '.join(p['topics'][:10])}")
        plines.append("")
        plines.append("## 外部链接")
        plines.append(f"- GitHub: [{p['full_name']}]({p['html_url']})")
        plines.append("")
        plines.append("## 反向链接")
        if mode == "weekday":
            plines.append(f"- [[Vibe-Coding-{today}|{today} 日报索引]]")
        else:
            plines.append(f"- [[AI-Weekly-{today}|{today} 周报索引]]")
        plines.append("")
        proj_file.write_text("\n".join(plines), encoding="utf-8")

    update_global_index(index_path, today, mode, projects)
    return index_path


def update_global_index(index_path, today, mode, projects):
    index_file = VAULT / "_Index.md"
    records = []
    if index_file.exists():
        content = index_file.read_text(encoding="utf-8")
        in_table = False
        for line in content.split("\n"):
            if line.startswith("| 日期"):
                in_table = True
                continue
            if in_table and line.startswith("|") and "---" not in line:
                cells = [c.strip() for c in line.strip("|").split("|")]
                if len(cells) >= 4 and cells[0] not in ("日期", ""):
                    records.append(cells[:4])

    # 避免重复
    if not any(r[0] == today for r in records):
        records.append([today, mode, str(len(projects)), f"[[{index_path.name}]]"])
    records.sort(key=lambda x: x[0], reverse=True)

    lines = []
    lines.append("---")
    lines.append("tags: [Index, AI, Trending]")
    lines.append("---")
    lines.append("")
    lines.append("# GitHub AI 项目归档索引")
    lines.append("")
    lines.append("| 日期 | 模式 | 项目数量 | 链接 |")
    lines.append("| --- | --- | --- | --- |")
    for r in records:
        lines.append(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} |")
    lines.append("")
    lines.append("## 项目索引")
    lines.append("")
    lines.append("| 项目 | 链接 |")
    lines.append("| --- | --- |")
    for p in projects:
        lines.append(f"| {p['full_name']} | [[{sanitize_filename(p['repo'])}|详情]] |")
    lines.append("")
    index_file.write_text("\n".join(lines), encoding="utf-8")


def build_wecom_message(projects, mode, today, weekday_cn):
    mode_label = "周报" if mode == "weekend" else "日报"
    msg = f"【GitHub AI 项目{mode_label}】\n"
    msg += f"日期：{today}（{weekday_cn}）\n"
    msg += f"共抓取 {len(projects)} 个项目：\n\n"
    for i, p in enumerate(projects, 1):
        desc = p.get("description", "") or ""
        if len(desc) > 60:
            desc = desc[:60] + "..."
        msg += f"{i}.{p['full_name']}（作者：{p['owner']}）\n"
        msg += f"简介：{desc}\n"
        msg += f"链接：{p['html_url']}\n\n"
    msg += "详细测试结果及完整笔记请查看 Obsidian 知识库。"

    # 长度控制
    if len(msg) > 2000:
        msg = f"【GitHub AI 项目{mode_label}】\n"
        msg += f"日期：{today}（{weekday_cn}）\n"
        msg += f"共抓取 {len(projects)} 个项目：\n\n"
        for i, p in enumerate(projects, 1):
            desc = p.get("description", "") or ""
            if len(desc) > 30:
                desc = desc[:30] + "..."
            msg += f"{i}.{p['full_name']}（作者：{p['owner']}）\n"
            msg += f"简介：{desc}\n"
            msg += f"链接：{p['html_url']}\n\n"
        msg += "详细测试结果及完整笔记请查看 Obsidian 知识库。"
    return msg


def save_wecom_message(msg, today):
    TMP.mkdir(parents=True, exist_ok=True)
    msg_file = TMP / f"wecom_message_{today}.txt"
    msg_file.write_text(msg, encoding="utf-8")
    return msg_file


def main():
    log_file = setup_logging()
    logging.info("=" * 50)
    logging.info("GitHub AI 项目归档任务启动")
    logging.info("=" * 50)

    weekday = datetime.now().weekday()
    mode = "weekend" if weekday >= 5 else "weekday"
    today = datetime.now().strftime("%Y-%m-%d")
    weekday_map = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    weekday_cn = weekday_map[weekday]

    logging.info(f"日期：{today}（{weekday_cn}），模式：{mode}")
    if not GITHUB_TOKEN:
        logging.warning("环境变量 GITHUB_TOKEN 未设置，将使用未认证请求（限额 60/h）")

    # 获取趋势项目
    repos = fetch_trending_repos(mode)
    if not repos:
        logging.error("未能获取 GitHub 趋势项目，任务终止")
        return 1

    # 工作日模式：Vibe Coding 关键词过滤，Top 5
    if mode == "weekday":
        filtered = []
        for r in repos:
            hay = f"{r['full_name']} {r['description']}".lower()
            if any(k in hay for k in VIBE_KEYWORDS):
                filtered.append(r)
        if filtered:
            repos = filtered
        else:
            logging.warning("未匹配到 Vibe Coding 关键词，使用全部 AI 项目")
        repos = repos[:5]
    else:
        repos = repos[:10]

    logging.info(f"待处理项目数：{len(repos)}")

    # 获取详情
    projects = []
    for r in repos:
        details = get_repo_details(r["owner"], r["repo"])
        if not details:
            logging.error(f"跳过 {r['full_name']}（获取详情失败）")
            continue
        weekly_growth = parse_stars_text(r.get("stars_text", ""))
        if weekly_growth == 0:
            # 基于总 Star 估算本周增量（粗略）
            weekly_growth = max(1, int(details.get("stargazers_count", 0) * 0.03))
        details["weekly_growth"] = weekly_growth
        details["readme_summary"] = get_readme_summary(r["owner"], r["repo"])
        projects.append(details)
        logging.info(
            f"[{len(projects)}] {details['full_name']} | 总 Star: {details['stargazers_count']} | "
            f"本周: +{weekly_growth} | 语言: {details['language']} | 描述: {details['description'][:50] if details['description'] else ''}"
        )

    if not projects:
        logging.error("所有项目详情获取失败，任务终止")
        return 1

    # 按本周新增 Star 降序
    projects.sort(key=lambda x: x.get("weekly_growth", 0), reverse=True)

    # 生成 Obsidian 文件
    index_path = generate_obsidian(projects, mode, today, weekday_cn)
    logging.info(f"已生成 Obsidian 索引：{index_path}")
    for p in projects:
        logging.info(f"已生成项目页：Projects/{sanitize_filename(p['repo'])}.md")

    # 构建并保存企业微信消息
    msg = build_wecom_message(projects, mode, today, weekday_cn)
    msg_file = save_wecom_message(msg, today)
    logging.info(f"企业微信消息已保存：{msg_file}")
    logging.info(f"消息长度：{len(msg)} 字符")

    # 保存结果摘要供外层读取
    summary = {
        "date": today,
        "mode": mode,
        "weekday": weekday_cn,
        "count": len(projects),
        "index_path": str(index_path),
        "msg_file": str(msg_file),
        "projects": [
            {
                "full_name": p["full_name"],
                "owner": p["owner"],
                "html_url": p["html_url"],
                "description": p.get("description", ""),
                "stargazers_count": p.get("stargazers_count", 0),
                "weekly_growth": p.get("weekly_growth", 0),
                "language": p.get("language", ""),
            }
            for p in projects
        ],
    }
    summary_file = TMP / f"task_summary_{today}.json"
    summary_file.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    logging.info(f"任务摘要已保存：{summary_file}")
    logging.info("=" * 50)
    logging.info(f"任务完成：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logging.info("=" * 50)
    return 0


if __name__ == "__main__":
    sys.exit(main())
