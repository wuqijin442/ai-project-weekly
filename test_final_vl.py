import json, time, urllib.request
op = urllib.request.build_opener(urllib.request.ProxyHandler({}))
BASE = "http://127.0.0.1:11434/v1/chat/completions"

TOOLS = [{"type":"function","function":{"name":"get_weather","description":"Get weather for a city","parameters":{"type":"object","properties":{"city":{"type":"string"}},"required":["city"]}}}]

# 1) plain generation
t0=time.time()
body={"model":"qwen3-vl:8b","messages":[{"role":"user","content":"用一句话解释什么是闭包。"}],"stream":False,"max_tokens":200}
req=urllib.request.Request(BASE,data=json.dumps(body).encode(),headers={"Content-Type":"application/json"},method="POST")
with op.open(req,timeout=120) as r:
    d=json.load(r)
wall=time.time()-t0
m=d["choices"][0]["message"]
print(f"[1] plain gen  wall={wall:.1f}s  content={repr((m.get('content') or '')[:80])}  finish={d['choices'][0].get('finish_reason')}")
print(f"    reasoning field present: {'reasoning' in m}  tok≈{len(m.get('content') or '')}")

# 2) tool call
t0=time.time()
body={"model":"qwen3-vl:8b","messages":[{"role":"user","content":"深圳今天天气怎么样？"}],"tools":TOOLS,"tool_choice":"auto","stream":False,"max_tokens":300}
req=urllib.request.Request(BASE,data=json.dumps(body).encode(),headers={"Content-Type":"application/json"},method="POST")
with op.open(req,timeout=120) as r:
    d=json.load(r)
wall=time.time()-t0
m=d["choices"][0]["message"]
print(f"[2] tool call  wall={wall:.1f}s  tool_calls={json.dumps(m.get('tool_calls'),ensure_ascii=False)}")
print(f"    content={repr((m.get('content') or '')[:40])}")

# 3) streaming sanity (count chunks, ensure content arrives)
t0=time.time()
body={"model":"qwen3-vl:8b","messages":[{"role":"user","content":"写一句 Python 问候语"}],"stream":True,"max_tokens":120}
req=urllib.request.Request(BASE,data=json.dumps(body).encode(),headers={"Content-Type":"application/json"},method="POST")
n=0; txt=""
with op.open(req,timeout=120) as r:
    for line in r:
        line=line.strip()
        if not line or line==b"data: [DONE]": continue
        if line.startswith(b"data: "): line=line[6:]
        try: c=json.loads(line)
        except: continue
        dl=c.get("choices",[{}])[0].get("delta",{})
        if dl.get("content"): txt+=dl["content"]; n+=1
wall=time.time()-t0
print(f"[3] stream    wall={wall:.1f}s  chunks={n}  text={repr(txt[:60])}")
