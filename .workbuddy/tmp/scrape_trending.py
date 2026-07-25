#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""抓取 GitHub Trending 页面并保存项目列表"""
import os
import re
import sys
import json
import logging
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from pathlib import Path

WORKSPACE = Path("D:/Users/Administrator/Desktop/AI Project Weekly")
LOGS = WORKSPACE / "logs"
TMP = WORKSPACE / ".workbuddy" / "tmp"

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
        description = desc_p.get_text(strip=True) if desc_p else ""
        lang_span = article.find("span", itemprop="programmingLanguage")
        language = lang_span.get_text(strip=True) if lang_span else ""
        stars_text = ""
        for tag in article.find_all(["span", "div"]):
            txt = tag.get_text(strip=True)
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


def fetch_trending_repos(mode):
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
        all_repos.extend(repos)
    if not all_repos:
        return []
    seen = set()
    unique = []
    for r in all_repos:
        if r["full_name"] not in seen:
            seen.add(r["full_name"])
            unique.append(r)
    filtered = []
    for r in unique:
        hay = f"{r['full_name']} {r['description']}".lower()
        if any(k in hay for k in AI_KEYWORDS):
            filtered.append(r)
    if not filtered:
        logging.warning("过滤后无 AI 项目，返回总榜全部项目")
        return unique
    return filtered


def main():
    setup_logging()
    logging.info("=" * 50)
    logging.info("开始抓取 GitHub Trending 项目列表")
    logging.info("=" * 50)

    weekday = datetime.now().weekday()
    mode = "weekend" if weekday >= 5 else "weekday"
    today = datetime.now().strftime("%Y-%m-%d")
    weekday_map = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    weekday_cn = weekday_map[weekday]

    logging.info(f"日期：{today}（{weekday_cn}），模式：{mode}")

    repos = fetch_trending_repos(mode)
    if not repos:
        logging.error("未能获取 GitHub 趋势项目")
        return 1

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

    TMP.mkdir(parents=True, exist_ok=True)
    output = {
        "date": today,
        "mode": mode,
        "weekday": weekday_cn,
        "count": len(repos),
        "repos": repos,
    }
    output_file = TMP / f"trending_repos_{today}.json"
    output_file.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    logging.info(f"已保存 {len(repos)} 个项目到 {output_file}")
    for i, r in enumerate(repos, 1):
        logging.info(f"{i}. {r['full_name']} - {r['description'][:60] if r['description'] else ''}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
