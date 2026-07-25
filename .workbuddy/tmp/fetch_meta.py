import json, os, base64, urllib.request, urllib.error

TMP = r"D:\Users\Administrator\Desktop\AI Project Weekly\.workbuddy\tmp"
TOKEN = os.environ.get("GITHUB_TOKEN", "")
trending = json.load(open(os.path.join(TMP, "trending_parsed.json"), encoding='utf-8'))
td = {d['full']: d for d in trending}

# Selected Top5 (protect strict: hallmark, openinterpreter; fill: skills, Vibe-Trading, dcg)
selected = ["mattpocock/skills", "Nutlope/hallmark", "HKUDS/Vibe-Trading",
            "Dicklesworthstone/destructive_command_guard", "openinterpreter/openinterpreter"]

def api(path):
    url = "https://api.github.com" + path
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "workbuddy-automation"
    })
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode('utf-8'))

results = []
for full in selected:
    try:
        repo = api(f"/repos/{full}")
    except Exception as e:
        print("REPO ERR", full, e); continue
    readme_txt = ""
    try:
        rm = api(f"/repos/{full}/readme")
        readme_txt = base64.b64decode(rm.get("content", "")).decode('utf-8', 'ignore')
    except Exception as e:
        print("README ERR", full, e)
    # weekly growth via stargazers history not available free; use star history fallback none
    entry = {
        "full": repo.get("full_name"),
        "owner": repo.get("owner", {}).get("login"),
        "repo": repo.get("name"),
        "url": repo.get("html_url"),
        "homepage": repo.get("homepage") or "",
        "description": repo.get("description") or td[full]['desc'],
        "stars": repo.get("stargazers_count"),
        "forks": repo.get("forks_count"),
        "open_issues": repo.get("open_issues_count"),
        "language": repo.get("language") or td[full]['lang'],
        "created_at": (repo.get("created_at") or "")[:10],
        "pushed_at": (repo.get("pushed_at") or "")[:10],
        "topics": repo.get("topics", []),
        "today": td[full]['today'],
        "period": td[full]['period'],
        "readme_excerpt": readme_txt[:2200],
    }
    results.append(entry)
    fn = os.path.join(TMP, f"meta_{entry['owner']}_{entry['repo']}.json")
    json.dump(entry, open(fn, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print(f"OK {full}: stars={entry['stars']} lang={entry['language']} created={entry['created_at']} topics={entry['topics'][:6]}")

json.dump(results, open(os.path.join(TMP, "selected_meta.json"), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print("SAVED selected_meta.json with", len(results), "entries")
