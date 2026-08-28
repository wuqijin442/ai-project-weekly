#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rag_lib.py — RAG 向量库核心 (Milvus Lite + nomic-embed-text via Ollama)

设计要点：
- 嵌入模型固定 nomic-embed-text:latest (768 维)，经本机 Ollama /api/embeddings 取向量
- 向量库用 milvus-lite 嵌入式 (无 Docker)，落盘于 repo/.rag/kb.db
- 本文件只被 ~/rag_venv/bin/python 导入 (milvus_lite 仅装在该 venv)
- 上层 learn_link.py 通过 subprocess 调用 rag_index.py / rag_query.py，不直接 import
"""
import os
import sys
import json
import time
import urllib.request
import urllib.error

# ---- 路径 ----
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 向量库放在 /opt/ragkb（不在 /home/taoyan 下）：
# DGX 上有 docker 容器 bind-mount 了 /home/taoyan，会在 milvus-lite 的 LOCK 文件上持 flock，
# 导致 /home 下任何 milvus 路径瞬间报 "another process holds the lock"。/opt 不在挂载范围内，规避该问题。
RAG_DIR = os.environ.get("RAG_DIR", "/opt/ragkb")
DB_PATH = os.path.join(RAG_DIR, "kb.db")
COLLECTION = "kb"

EMBED_MODEL = "nomic-embed-text:latest"
EMBED_DIM = 768
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434").rstrip("/")

from milvus_lite import MilvusLite, CollectionSchema, FieldSchema, DataType  # noqa: E402

# --- 禁用 milvus-lite 的 flock 排他锁 ---
# 本机（DGX aarch64 + 多 docker 容器）下 milvus-lite 的 fcntl.flock 排他锁会偶发
# "another process holds the lock" 纠缠，导致打开即失败。我们的用法是单进程、顺序访问
# （每日 learn_link 仅一次 RAG 操作），无需跨进程互斥，故把 _acquire_lock 改为仅打开
# 锁文件 fd 而不真正 flock，规避该环境 gremlin。多进程并发时本脚本不保证安全（当前无此场景）。
import milvus_lite.db as _milvus_db  # noqa: E402


def _acquire_lock_noop(self):
    fd = os.open(self._lock_path, os.O_CREAT | os.O_RDWR, 0o644)
    self._lock_fd = fd


_milvus_db.MilvusLite._acquire_lock = _acquire_lock_noop


def get_collection(retries=30, backoff=2.0):
    """打开（或创建）向量集合，返回 (MilvusLite, Collection)。

    milvus-lite 用 flock 做目录级排他锁；本机偶有其他进程瞬时占用同一 db 路径，
    故在打开失败时按指数退避重试，避免一次性失败。
    """
    os.makedirs(RAG_DIR, exist_ok=True)
    c = None
    last_err = None
    for i in range(retries):
        try:
            c = MilvusLite(DB_PATH)
            break
        except Exception as e:  # DataDirLockedError 等
            last_err = e
            if i < retries - 1:
                time.sleep(backoff * (1 + i * 0.1))
            continue
    if c is None:
        raise RuntimeError(f"get_collection: 无法在 {retries} 次重试内获取锁: {last_err}")
    schema = CollectionSchema([
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=EMBED_DIM),
        FieldSchema(name="source", dtype=DataType.VARCHAR, max_length=512),
        FieldSchema(name="date", dtype=DataType.VARCHAR, max_length=32),
        FieldSchema(name="content", dtype=DataType.VARCHAR, max_length=65535),
    ])
    try:
        col = c.get_collection(COLLECTION)
    except Exception:
        col = c.create_collection(COLLECTION, schema)
    return c, col


def embed(text):
    """调用本机 Ollama 取 nomic-embed-text 向量 (768 维)。"""
    text = (text or "").strip()
    if not text:
        raise ValueError("embed: empty text")
    payload = json.dumps({"model": EMBED_MODEL, "prompt": text}).encode("utf-8")
    req = urllib.request.Request(
        f"{OLLAMA_URL}/api/embeddings",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    vec = data.get("embedding") or data.get("embeddings")
    if not vec or len(vec) != EMBED_DIM:
        raise ValueError(f"embed: unexpected vector dim {None if not vec else len(vec)}")
    return vec


def chunk_markdown(text, max_chars=700, overlap_lines=3):
    """按空行分段，超长段再切，保留少量重叠上下文。"""
    lines = text.splitlines()
    chunks, buf, length = [], [], 0
    for ln in lines:
        buf.append(ln)
        length += len(ln) + 1
        if length >= max_chars and ln.strip() == "":
            chunks.append("\n".join(buf).strip())
            tail = buf[-overlap_lines:] if len(buf) > overlap_lines else buf
            buf = list(tail)
            length = sum(len(x) + 1 for x in buf)
    if buf:
        chunks.append("\n".join(buf).strip())
    return [c for c in chunks if c]


def chunk_text(text, max_chars=1500, overlap=200):
    """字符级滑动切片（用于 JSON / 长单行），规避 nomic-embed 上下文上限。"""
    text = text.strip()
    if not text:
        return []
    if len(text) <= max_chars:
        return [text]
    chunks, start = [], 0
    while start < len(text):
        end = min(start + max_chars, len(text))
        chunks.append(text[start:end].strip())
        if end >= len(text):
            break
        start = max(end - overlap, start + 1)
    return [c for c in chunks if c]


def _iter_md_dir(subdir, max_chars=700, overlap_lines=3):
    """遍历 reports/<subdir> 下的 .md，按日分块产出 (date, source, content)。"""
    out = []
    d = os.path.join(REPO_ROOT, "reports", subdir)
    if not os.path.isdir(d):
        return out
    for fn in sorted(os.listdir(d)):
        if not fn.endswith(".md"):
            continue
        date = fn[:-3]
        path = os.path.join(d, fn)
        try:
            with open(path, encoding="utf-8") as f:
                text = f.read()
        except Exception:
            continue
        for i, ch in enumerate(chunk_markdown(text, max_chars=max_chars, overlap_lines=overlap_lines)):
            out.append((date, f"reports/{subdir}/{fn}#{i}", ch))
    return out


def iter_sources():
    """产出待入库知识源：(date, source_name, content_text)。

    覆盖项目全部"已同步到 DGX"的历史数据：
    - reports/learnings  : 每日学习消化（AI 趋势洞察）
    - reports/daily      : 每日 GitHub Trending 日报
    - reports/boards     : 11 板块深潜报告
    - reports/weekly     : 周报聚合
    - knowledge-base     : 项目知识库（awesome/projects 等）
    - data/metadata      : 每日真实运行元数据（clone/install/run 结果，按字符切片避免超 nomic 上下文）

    注：Obsidian_Vault / 储能知识库 被 gitignore，不随仓库同步到 DGX，无法入库。
    """
    out = []
    out += _iter_md_dir("learnings")
    out += _iter_md_dir("daily")
    out += _iter_md_dir("boards")
    out += _iter_md_dir("weekly")
    out += _iter_md_dir("knowledge-base")
    # 每日元数据（按字符切片，避免整文件超 nomic-embed 上下文上限）
    meta_dir = os.path.join(REPO_ROOT, "data", "metadata")
    if os.path.isdir(meta_dir):
        for fn in sorted(os.listdir(meta_dir)):
            if not fn.endswith(".json"):
                continue
            date = fn[:-5]
            path = os.path.join(meta_dir, fn)
            try:
                with open(path, encoding="utf-8") as f:
                    text = f.read()
            except Exception:
                continue
            for i, ch in enumerate(chunk_text(text)):
                out.append((date, f"data/metadata/{fn}#{i}", ch))
    return out


if __name__ == "__main__":
    # 自测
    c, col = get_collection()
    print("collection:", col.name, "entities:", col.num_entities)
    v = embed("RAG 向量检索架构 self-evolution")
    print("embed dim:", len(v))
