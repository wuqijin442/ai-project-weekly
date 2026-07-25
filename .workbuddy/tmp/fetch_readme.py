import json, subprocess, os, base64, sys, time, re

TOKEN = os.environ.get("GITHUB_TOKEN", "")
api = json.load(open(".workbuddy/tmp/api_details.json"))
repos = list(api.keys())

def get_readme(repo):
    url = f"https://api.github.com/repos/{repo}/readme"
    cmd = ["curl","-s","-m","25","-H","Accept: application/vnd.github+json",
           "-H",f"Authorization: Bearer {TOKEN}","-w","\n__HTTP__%{http_code}",url]
    res = subprocess.run(cmd, capture_output=True, text=True)
    body = res.stdout
    http="?"
    if "__HTTP__" in body:
        body,http=body.rsplit("__HTTP__",1)
    try:
        d=json.loads(body)
    except Exception:
        return "", http
    if "content" not in d:
        return "", http
    try:
        txt=base64.b64decode(d["content"]).decode("utf-8","ignore")
    except Exception:
        return "", http
    # clean: take first ~1200 chars of meaningful text
    txt=re.sub(r'!\[[^\]]*\]\([^)]*\)','',txt)  # images
    txt=re.sub(r'<[^>]+>','',txt)
    return txt, http

out={}
for r in repos:
    txt,http=get_readme(r)
    out[r]=txt[:1600]
    print(f"{r}: http={http} len={len(txt)}", file=sys.stderr)
    time.sleep(0.3)

json.dump(out, open(".workbuddy/tmp/readmes.json","w"), ensure_ascii=False, indent=2)
print("DONE", file=sys.stderr)
