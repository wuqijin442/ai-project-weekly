#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rag_query.py — 检索相关历史知识片段 (供 learn_link.py 注入上下文)

用法:
    ~/rag_venv/bin/python src/rag_query.py --query "..." [--top-k 5] [--min-date 2026-08-01]

输出: JSON 数组 (写到 stdout)，每项 {source, date, content, distance}
无任何结果或异常时输出空数组 []，调用方安全解析。
"""
import os
import sys
import json
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rag_lib  # noqa: E402


def query(q, top_k=5, min_date=None):
    try:
        vec = rag_lib.embed(q)
    except Exception as e:
        print(f"[]  # embed failed: {e}", file=sys.stderr)
        return []
    try:
        c, col = rag_lib.get_collection()
        col.load()
    except Exception as e:
        print(f"[]  # milvus open failed: {e}", file=sys.stderr)
        return []
    try:
        res = col.search(
            query_vectors=[vec],
            top_k=top_k,
            anns_field="vector",
            output_fields=["source", "date", "content"],
            metric_type="COSINE",
        )
    except Exception as e:
        print(f"[]  # search failed: {e}", file=sys.stderr)
        return []
    hits = res[0] if res else []
    out = []
    for h in hits:
        ent = h.get("entity", {})
        src = ent.get("source", "")
        if min_date and ent.get("date", "") < min_date:
            continue
        out.append({
            "source": src,
            "date": ent.get("date", ""),
            "content": ent.get("content", ""),
            "distance": round(float(h.get("distance", 0.0)), 4),
        })
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--query", required=True)
    ap.add_argument("--top-k", type=int, default=5)
    ap.add_argument("--min-date", default=None)
    args = ap.parse_args()
    out = query(args.query, args.top_k, args.min_date)
    print(json.dumps(out, ensure_ascii=False, indent=2))
