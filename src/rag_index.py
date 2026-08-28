#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rag_index.py — 将知识源灌入 Milvus 向量库 (增量，按 source 去重)

用法:
    ~/rag_venv/bin/python src/rag_index.py [--force]

--force: 先清空整个集合再全量重建
依赖: milvus_lite (仅 ~/rag_venv 内有) + 本机 Ollama nomic-embed-text
"""
import os
import sys
import json
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rag_lib  # noqa: E402


def safe_source(expr_source):
    s = expr_source.replace("\\", "\\\\").replace('"', '\\"')
    return s


def rebuild(force):
    c, col = rag_lib.get_collection()
    if force:
        try:
            col.release()
        except Exception:
            pass
        try:
            c.drop_collection(rag_lib.COLLECTION)
        except Exception:
            pass
        c, col = rag_lib.get_collection()

    sources = rag_lib.iter_sources()
    total, ok, skipped = len(sources), 0, 0
    BATCH = 32
    for i in range(0, len(sources), BATCH):
        batch = sources[i:i + BATCH]
        rows, has_err = [], False
        for date, src, content in batch:
            try:
                vec = rag_lib.embed(content)
            except Exception as e:
                print(f"  [skip] embed failed: {src} -> {e}", file=sys.stderr)
                has_err = True
                continue
            rows.append({
                "vector": vec,
                "source": src[:512],
                "date": date[:32],
                "content": content[:65535],
            })
        if not rows:
            continue
        # 去重：删除本批涉及的旧 source 行，再插入新行
        seen = {}
        for r in rows:
            seen[r["source"]] = True
        for src in seen:
            try:
                col.delete(expr=f'source == "{safe_source(src)}"')
            except Exception:
                pass
        try:
            col.insert(rows)
            ok += len(rows)
        except Exception as e:
            print(f"  [err] insert batch failed: {e}", file=sys.stderr)
            has_err = True
        if has_err:
            skipped += 1
        col.flush()
        print(f"  ingested {min(i + BATCH, total)}/{total}  (rows ok={ok})", flush=True)

    print(f"DONE total={total} inserted={ok} batches_with_skip={skipped} entities={col.num_entities}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true", help="drop and rebuild from scratch")
    args = ap.parse_args()
    rebuild(args.force)
