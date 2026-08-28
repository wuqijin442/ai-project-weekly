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

    sources = rag_lib.iter_sources(include_extra=True)
    raw_total = len(sources)
    total = raw_total

    if not force:
        # 增量：跳过已在集合中的文件（按 source 前缀判断），只追加新文件。
        # 这样每日 learn_link 不会重复吃满全量历史，也不会因 dgx 工作树不完整而丢失历史
        # （全量历史已在首次 --force 重建时一次性灌入）。
        existing = rag_lib.existing_source_prefixes(col)
        if existing:
            sources = [s for s in sources if s[1].split("#", 1)[0] not in existing]
        total = len(sources)
        if not sources:
            print(f"DONE (incremental) candidates={raw_total} new=0  nothing to ingest")
            return

    ok, skipped = 0, 0
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
        # 去重：先按 source 查出主键 id，再按 id 删除旧行，最后插入新行。
        # 注意 milvus-lite 的 delete 只接受 pks（不接受 expr），故先 query 取 id。
        seen = {}
        for r in rows:
            seen[r["source"]] = True
        for src in seen:
            try:
                old = col.query(
                    expr=f'source == "{safe_source(src)}"',
                    output_fields=["id"],
                    limit=100000,
                )
                if old:
                    col.delete(pks=[o["id"] for o in old])
            except Exception as e:
                print(f"  [warn] dedup delete failed for {src}: {e}", file=sys.stderr)
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

    mode = "force(full-rebuild)" if force else "incremental"
    print(f"DONE mode={mode} candidates={raw_total} ingested={total} inserted_rows={ok} batches_with_skip={skipped} entities={col.num_entities}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true", help="drop and rebuild from scratch")
    args = ap.parse_args()
    rebuild(args.force)
