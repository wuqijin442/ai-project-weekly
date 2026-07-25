import re, json, sys

html = open(sys.argv[1], encoding='utf-8').read()

# Split by article Box-row blocks (GitHub trending uses <article ...> per repo)
# Be robust to tmp- prefix obfuscation: split on '<article'
parts = re.split(r'<article[^>]*>', html)
repos = []
for blk in parts[1:]:
    # repo full name: first href matching /owner/repo pattern where the text has no / in path beyond 2 segments
    # The repo link is <a href="/owner/repo" ...>owner / repo</a> with whitespace
    m = re.search(r'href="(/[^"/]+/[^"/]+)"', blk)
    if not m:
        continue
    full = m.group(1).strip('/')
    if full.count('/') != 1:
        continue
    owner, repo = full.split('/')
    # description
    dm = re.search(r'<p[^>]*class="[^"]*col-9[^"]*"[^>]*>(.*?)</p>', blk, re.S)
    desc = ''
    if dm:
        desc = re.sub(r'<[^>]+>', '', dm.group(1))
        desc = re.sub(r'\s+', ' ', desc).strip()
    # stars total: link to /stargazers
    sm = re.search(r'href="/'+re.escape(full)+r'/stargazers"[^>]*>\s*(.*?)\s*</a>', blk, re.S)
    stars = None
    if sm:
        s = re.sub(r'<[^>]+>', '', sm.group(1))
        stars = s.strip()
    # today / this week growth: text like "1,234 stars today" or "stars this week"
    today = None
    week = None
    gm = re.search(r'([\d,]+)\s+stars\s+(today|this week)', blk)
    if gm:
        val = int(gm.group(1).replace(',', ''))
        if gm.group(2) == 'today':
            today = val
        else:
            week = val
    # language
    lm = re.search(r'<span[^>]*itemprop="programmingLanguage"[^>]*>(.*?)</span>', blk, re.S)
    lang = re.sub(r'<[^>]+>', '', lm.group(1)).strip() if lm else None
    repos.append({
        'full': full, 'owner': owner, 'repo': repo,
        'desc': desc, 'stars': stars, 'today': today,
        'week': week, 'lang': lang
    })

print(json.dumps(repos, ensure_ascii=False, indent=2))
print("TOTAL:", len(repos), file=sys.stderr)
