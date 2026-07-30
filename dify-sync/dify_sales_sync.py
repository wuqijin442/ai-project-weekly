#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
韬延销售资料 -> Dify 知识库 增量同步脚本（方案B：RAG 进化）
运行环境：能访问群晖 \\\\Taoke_server\\韬延-销售资料 且能访问 Dify API 的 Windows 机器
效果：把群晖销售资料增量同步进 Dify 知识库，模型(taoyan-ess)无需重建即可用上最新资料

配置（环境变量，或改下方 DEFAULTS）：
  DIFY_BASE_URL   默认 http://192.168.0.121/v1
  DIFY_API_KEY    必填！Dify 右上角头像 -> 设置 -> API Keys 生成
  SOURCE_DIR      默认 \\\\Taoke_server\\韬延-销售资料
  DATASET_NAME    默认 "韬延储能知识库"（存在则复用，否则自动创建）
  STATE_FILE      默认脚本同目录 .state.json（记录已同步文件 hash+doc_id）

依赖：pip install requests
运行：
  set DIFY_API_KEY=app-xxxx
  python dify_sales_sync.py
定时进化：Windows 任务计划程序每天 03:30 跑一次即可随群晖数据更新
"""
import os
import sys
import json
import hashlib
import time
import requests
from pathlib import Path


def load_local_env():
    """读取脚本同目录 .env（不依赖 python-dotenv），避免把 Key 写进源码/提交。
    .gitignore 已忽略 *.env，Key 不会随项目同步到 GitHub。"""
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if not os.path.exists(p):
        return
    with open(p, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())
    print(f"[{time.strftime('%H:%M:%S')}] 已从 .env 载入配置", flush=True)


load_local_env()  # 必须在读取下方配置前调用

# ---------------- 配置 ----------------
DEFAULTS = {
    "DIFY_BASE_URL": "http://192.168.0.121/v1",
    "DIFY_API_KEY": "",
    "SOURCE_DIR": r"\\Taoke_server\韬延-销售资料",
    "DATASET_NAME": "韬延储能知识库",
    "STATE_FILE": str(Path(__file__).with_suffix(".state.json")),
}
DIFY_BASE_URL = os.getenv("DIFY_BASE_URL", DEFAULTS["DIFY_BASE_URL"]).rstrip("/")
DIFY_API_KEY = os.getenv("DIFY_API_KEY", DEFAULTS["DIFY_API_KEY"])
SOURCE_DIR = os.getenv("SOURCE_DIR", DEFAULTS["SOURCE_DIR"])
DATASET_NAME = os.getenv("DATASET_NAME", DEFAULTS["DATASET_NAME"])
STATE_FILE = os.getenv("STATE_FILE", DEFAULTS["STATE_FILE"])

# Dify 支持的文件类型（索引用）
ALLOWED_EXT = {
    ".txt", ".md", ".markdown", ".pdf", ".docx", ".doc",
    ".xlsx", ".xls", ".csv", ".html", ".json", ".pptx",
}
# Dify 单文件默认上限 15MB（超过跳过，避免索引失败）
MAX_FILE_BYTES = 15 * 1024 * 1024

HEADERS = {"Authorization": f"Bearer {DIFY_API_KEY}"}
STATE = {}  # rel_path -> {"hash":..., "doc_id":...}


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def load_state():
    global STATE
    if os.path.exists(STATE_FILE):
        try:
            STATE = json.load(open(STATE_FILE, encoding="utf-8"))
        except Exception as e:
            log(f"状态文件损坏，重置：{e}")
            STATE = {}
    else:
        STATE = {}


def save_state():
    json.dump(STATE, open(STATE_FILE, "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)


def file_hash(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def get_or_create_dataset():
    """按名称找知识库，找不到则新建（high_quality 用已配置的 nomic-embed-text）"""
    url = f"{DIFY_BASE_URL}/datasets"
    page = 1
    while True:
        r = requests.get(url, headers=HEADERS,
                         params={"page": page, "limit": 100}, timeout=30)
        r.raise_for_status()
        data = r.json().get("data", [])
        for ds in data:
            if ds.get("name") == DATASET_NAME:
                log(f"命中已有知识库: {ds['name']} ({ds['id']})")
                return ds["id"]
        if len(data) < 100:
            break
        page += 1
    # 新建
    r = requests.post(url, headers=HEADERS, json={
        "name": DATASET_NAME,
        "permission": "only_me",
        "indexing_technique": "high_quality",
        "embedding_model": "nomic-embed-text",
    }, timeout=60)
    r.raise_for_status()
    ds_id = r.json()["id"]
    log(f"已新建知识库: {DATASET_NAME} ({ds_id})")
    return ds_id


def find_doc_id_by_name(dataset_id, rel_name):
    """在 dataset 文档里按名称找 doc_id（用于更新/删除时定位）"""
    url = f"{DIFY_BASE_URL}/datasets/{dataset_id}/documents"
    page = 1
    while True:
        r = requests.get(url, headers=HEADERS,
                         params={"page": page, "limit": 100}, timeout=30)
        r.raise_for_status()
        data = r.json().get("data", [])
        for d in data:
            if d.get("name") == rel_name:
                return d["id"]
        if len(data) < 100:
            break
        page += 1
    return None


def delete_doc(dataset_id, doc_id):
    if not doc_id:
        return
    url = f"{DIFY_BASE_URL}/datasets/{dataset_id}/documents/{doc_id}"
    try:
        r = requests.delete(url, headers=HEADERS, timeout=30)
        r.raise_for_status()
        log(f"已删除旧文档 {doc_id}")
    except Exception as e:
        log(f"删除文档失败 {doc_id}: {e}")


def upload_file(dataset_id, full_path, rel_name):
    url = f"{DIFY_BASE_URL}/datasets/{dataset_id}/document/create-by-file"
    try:
        with open(full_path, "rb") as f:
            files = {"file": (os.path.basename(full_path), f,
                              "application/octet-stream")}
            data = {
                "data": json.dumps({
                    "name": rel_name,
                    "indexing_technique": "high_quality",
                    "process_rule": {"mode": "automatic"},
                })
            }
            r = requests.post(url, headers=HEADERS, files=files,
                              data=data, timeout=180)
        r.raise_for_status()
        doc = r.json().get("document", {})
        log(f"上传成功: {rel_name} -> doc_id={doc.get('id')}")
        return doc.get("id")
    except Exception as e:
        log(f"上传失败: {rel_name} | {e}")
        if r is not None:
            log(f"  resp: {r.text[:300]}")
        return None


def scan_source():
    """返回 {rel_name: md5} 仅含允许类型且未超大的文件"""
    current = {}
    if not os.path.isdir(SOURCE_DIR):
        log(f"源目录不存在: {SOURCE_DIR}")
        return current
    for root, _, files in os.walk(SOURCE_DIR):
        for fn in files:
            ext = os.path.splitext(fn)[1].lower()
            if ext not in ALLOWED_EXT:
                continue
            full = os.path.join(root, fn)
            try:
                size = os.path.getsize(full)
            except OSError:
                continue
            if size > MAX_FILE_BYTES:
                log(f"跳过(超15MB): {full}")
                continue
            rel = os.path.relpath(full, SOURCE_DIR).replace("\\", "/")
            current[rel] = file_hash(full)
    return current


def main():
    if not DIFY_API_KEY:
        log("ERROR: 未设置 DIFY_API_KEY。请在 Dify 设置生成 API Key 后 "
            "用 `set DIFY_API_KEY=app-xxxx` 再运行。")
        sys.exit(1)
    load_state()
    dataset_id = get_or_create_dataset()
    current = scan_source()
    log(f"扫描到源文件 {len(current)} 个（允许类型内）")

    # 1) 新增 / 更新
    for rel, h in current.items():
        old = STATE.get(rel)
        if old and old.get("hash") == h:
            continue  # 未变，跳过
        if old and old.get("doc_id"):
            delete_doc(dataset_id, old["doc_id"])  # 先删旧版
        doc_id = upload_file(dataset_id, os.path.join(SOURCE_DIR, rel), rel)
        STATE[rel] = {"hash": h, "doc_id": doc_id}

    # 2) 源已删除的文件 -> 清理知识库
    for rel in list(STATE.keys()):
        if rel not in current:
            delete_doc(dataset_id, STATE[rel].get("doc_id"))
            del STATE[rel]

    save_state()
    log("同步完成。知识库已与群晖销售资料对齐，taoyan-ess 经 Dify RAG 即可用最新资料。")


if __name__ == "__main__":
    main()
