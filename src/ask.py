#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ask.py — 基于私有知识库（Milvus Lite RAG）的专属问答命令行

用法:
    ~/rag_venv/bin/python src/ask.py "你的问题"
    ~/rag_venv/bin/python src/ask.py            # 无参数则进入交互式逐行提问

行为:
    1. 用问题做向量检索（rag_retrieve，搜全量知识库，不限日期）
    2. 把 top-K 相关片段 + 问题交给本地 qwen3.8:27b 生成带出处的回答
    3. 打印回答 + 参考来源列表

依赖: 复用 learn_link.rag_retrieve / call_ollama（与每日 learn_link 同链路）。
注: 仅依赖 Python 标准库；rag_query 经 RAG_VENV_PY 子进程调用（需 ~/rag_venv）。
"""
import os
import sys
import re

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from learn_link import rag_retrieve, call_ollama, MODEL  # noqa: E402


def strip_think(text):
    if not text:
        return ""
    return re.sub(r"<thinking>.*?</think>", "", text, flags=re.DOTALL).strip()


SYSTEM_PROMPT = (
    "你是一个严格基于「用户私有知识库」作答的助手。知识库内容来自用户的 Obsidian 笔记、"
    "储能知识库、以及 AI Project Weekly 的每日/板块/周报历史。\n"
    "规则：\n"
    "1. 只依据下面提供的【参考上下文】回答，禁止编造上下文之外的信息或项目。\n"
    "2. 每个关键结论尽量标注出处（引用上下文里的 source 文件名/日期）。\n"
    "3. 若上下文不足以回答，明确说「知识库中未找到相关内容」，不要猜测。\n"
    "4. 用中文、简洁、结构化作答；不输出思考过程标签。\n"
)


def ask(question, top_k=5):
    print(f"[检索] 问题: {question}", flush=True)
    print(f"[检索] 使用模型: {MODEL}", flush=True)
    hits = rag_retrieve(question, top_k=top_k)
    if not hits:
        print("[警告] 知识库中未检索到相关内容，无法基于私有知识作答。")
        return

    ctx = []
    for i, h in enumerate(hits):
        src = h.get("source", "")
        content = (h.get("content") or "")[:1200]
        ctx.append(f"[{i + 1}] (来源: {src})\n{content}")
    context = "\n\n".join(ctx)

    user_msg = f"【参考上下文】\n{context}\n\n【用户问题】\n{question}\n"
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_msg},
    ]
    answer = call_ollama(messages)
    answer = strip_think(answer)

    print("\n[回答]")
    print(answer or "（模型无返回）")
    print("\n[参考来源]")
    for i, h in enumerate(hits):
        dist = h.get("distance", 0)
        print(f"  {i + 1}. {h.get('source', '')}  (dist={dist:.3f})")


def main():
    if len(sys.argv) > 1:
        q = " ".join(sys.argv[1:]).strip()
        if q:
            ask(q)
            return
    # 无参数：交互式
    print("专属知识问答（输入空行或 Ctrl-C 退出）")
    while True:
        try:
            q = input("问知识库> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n再见")
            break
        if not q:
            continue
        ask(q)
        print()


if __name__ == "__main__":
    main()
