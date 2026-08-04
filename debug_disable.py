import json, urllib.request
op = urllib.request.build_opener(urllib.request.ProxyHandler({}))
BASE="http://127.0.0.1:11434/v1/chat/completions"

variants = {
    "think:false":         {"think": False},
    "reasoning:false":     {"reasoning": False},
    "enable_thinking:false":{"enable_thinking": False},
    "chat_template_kwargs": {"chat_template_kwargs": {"enable_thinking": False}},
}
for name, extra in variants.items():
    body={"model":"qwen3-vl:8b","messages":[{"role":"user","content":"用一句话解释闭包。"}],"stream":False,"max_tokens":200}
    body.update(extra)
    req=urllib.request.Request(BASE,data=json.dumps(body).encode(),headers={"Content-Type":"application/json"},method="POST")
    try:
        with op.open(req,timeout=120) as r:
            d=json.load(r)
        m=d["choices"][0]["message"]
        print(f"\n=== {name} ===")
        print(" content:", repr((m.get('content') or '')[:100]))
        print(" reasoning:", repr((m.get('reasoning') or '')[:100]))
        print(" finish:", d["choices"][0].get("finish_reason"), " usage:", d.get("usage"))
    except Exception as e:
        print(f"ERR {name}: {e}")
