import json, subprocess, sys, os, time

TOKEN = os.environ.get("GITHUB_TOKEN", "")
repos = ["tirth8205/code-review-graph", "KnockOutEZ/wigolo", "1jehuang/jcode",
         "MoonshotAI/kimi-cli", "PrefectHQ/fastmcp"]

out = {}
for r in repos:
    url = f"https://api.github.com/repos/{r}"
    cmd = ["curl", "-s", "-m", "25", "-H", "Accept: application/vnd.github+json",
           "-H", f"Authorization: Bearer {TOKEN}", "-w", "\n__HTTP__%{http_code}", url]
    res = subprocess.run(cmd, capture_output=True, text=True)
    body = res.stdout
    http = "?"
    if "__HTTP__" in body:
        body, http = body.rsplit("__HTTP__", 1)
    try:
        d = json.loads(body)
    except Exception as e:
        print(f"{r}: HTTP={http} PARSE_FAIL {e}", file=sys.stderr)
        out[r] = {"error": str(e), "http": http}
        continue
    if "message" in d and "rate limit" in str(d.get("message", "")).lower():
        print(f"{r}: HTTP={http} RATE_LIMITED", file=sys.stderr)
        out[r] = {"error": "rate_limited", "http": http}
        break
    info = {
        "created_at": d.get("created_at", "")[:10],
        "stars": d.get("stargazers_count"),
        "forks": d.get("forks_count"),
        "language": d.get("language"),
        "topics": d.get("topics", []),
        "homepage": d.get("homepage", ""),
        "description": d.get("description", ""),
        "open_issues": d.get("open_issues_count"),
        "pushed_at": d.get("pushed_at", "")[:10],
    }
    out[r] = info
    print(f"{r}: HTTP={http} created={info['created_at']} stars={info['stars']} lang={info['language']} topics={info['topics'][:6]}", file=sys.stderr)
    time.sleep(0.3)

json.dump(out, open(".workbuddy/tmp/api_details.json", "w"), ensure_ascii=False, indent=2)
print("DONE", file=sys.stderr)
