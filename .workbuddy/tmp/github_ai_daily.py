import re, html, json, os, sys

TMP = r"D:\Users\Administrator\Desktop\AI Project Weekly\.workbuddy\tmp"
HTML = os.path.join(TMP, "trending_daily.html")
OUT = os.path.join(TMP, "trending_parsed.json")

def parse(path):
    with open(path, encoding='utf-8', errors='ignore') as f:
        s = f.read()
    rows = re.findall(r'<article class="Box-row">(.*?)</article>', s, re.S)
    out = []
    for r in rows:
        m = re.search(r'<h2[^>]*>\s*<a[^>]*href="/([^"]+)"', r)
        if not m:
            m = re.search(r'href="/([^"/]+/[^"]+?)"', r)
        full = m.group(1).strip() if m else None
        if not full or full.count('/') != 1:
            continue
        owner, repo = full.split('/', 1)
        d = re.search(r'<p[^>]*class="[^"]*col-9[^"]*"[^>]*>(.*?)</p>', r, re.S)
        desc = ''
        if d:
            desc = re.sub(r'<[^>]+>', '', d.group(1))
            desc = html.unescape(desc).strip()
        stars = re.search(r'href="/[^"]+/stargazers"[^>]*>\s*(.*?)\s*</a>', r, re.S)
        total = ''
        if stars:
            total = re.sub(r'<[^>]+>', '', stars.group(1)).replace(',', '').strip()
        today = re.search(r'([\d,]+)\s+stars\s+(today|this week)', r)
        today_n = today.group(1).replace(',', '') if today else ''
        period = today.group(2) if today else ''
        lang = re.search(r'itemprop="programmingLanguage">([^<]+)</span>', r)
        language = lang.group(1).strip() if lang else ''
        out.append({'full': full, 'owner': owner, 'repo': repo,
                    'url': 'https://github.com/' + full, 'desc': desc,
                    'stars': total, 'today': today_n, 'period': period, 'lang': language})
    return out

KEYWORDS = ["cursor","cline","aider","continue","swe-agent","open-interpreter",
            "browser-use","gpt-engineer","meta-gpt","devin","autocode","copilot",
            "cli-agent","code-generator","llm-dev"]
ECOS = ["claude","codex","cursor","mcp","agent","skill","copilot","coding agent","llm agent","vibe coding","ai coding"]

def norm(t): return (t or "").lower()

data = parse(HTML)
json.dump(data, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print("PARSED_COUNT:", len(data))

print("\n=== STRICT KEYWORD HITS ===")
strict = []
for d in data:
    blob = norm(d['full']) + " " + norm(d['desc'])
    hits = [k for k in KEYWORDS if re.search(r'(?<![a-z])' + re.escape(k) + r'(?![a-z])', blob)]
    if hits:
        strict.append((d, hits))
        print(f"  {d['full']:45s} today={int(d['today'] or 0):>5} hits={hits}")

print("\n=== ECOSYSTEM EXPANSION CANDIDATES ===")
exp = []
for d in data:
    if any(d is s[0] for s in strict):
        continue
    blob = norm(d['full']) + " " + norm(d['desc'])
    sig = [e for e in ECOS if e in blob]
    if sig:
        exp.append((d, sig))
        print(f"  {d['full']:45s} today={int(d['today'] or 0):>5} signals={sig}")

print("\n=== ALL SORTED BY TODAY ===")
for i, d in enumerate(sorted(data, key=lambda x: int(x['today'] or 0), reverse=True), 1):
    print(f"  {i:2d}. {d['full']:45s} today={int(d['today'] or 0):>5} stars={d['stars']:>7} lang={d['lang']}")
