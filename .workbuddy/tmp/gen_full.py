import json
raw = json.load(open('.workbuddy/tmp/all_projects.json', encoding='utf-8'))

def _stars(r):
    try:
        return int(r.get('stars') or 0)
    except (ValueError, TypeError):
        return 0

def _key(alias):
    return alias.split(',')[0].strip().lower().replace(' ', '-')

# Dedup by normalized repo key: keep the higher-star (most recent) entry.
best = {}
dropped = []
for r in raw:
    k = _key(r['alias'])
    if k in best:
        if _stars(r) > _stars(best[k]):
            dropped.append(best[k]); best[k] = r
        else:
            dropped.append(r)
    else:
        best[k] = r
rows = list(best.values())
N_UNIQUE = len(rows)
deduped_from = len(raw) - N_UNIQUE

def classify(r):
    blob = (r['tags'] + " " + r['alias'] + " " + r['file']).lower()
    if any(k in blob for k in ["ai-gateway", "llm-router", "omniroute"]):
        return "A"
    if any(k in blob for k in ["coding-agent", "cli-agent", "tui", "terminal",
        "codex", "openinterpreter", "swe-agent", "aider", "gpt-engineer", "cline", "continue",
        "jcode", "kimi-cli", "background-agents", "codexbar", "claude-video", "herdr",
        "planning-with-files", "dcg", "copilot-sdk", "agent harness", "coding agent"]):
        return "D"
    if any(k in blob for k in ["skill", "skills", "prompt", "claude-skills", "spec-kit",
        "design.md", "hallmark", "superpowers", "marketingskills", "graphify", "i-have-adhd",
        "last30days", "system_prompts", "claude-code-templates", "cwc-workshops"]):
        return "C"
    if any(k in blob for k in ["code-review", "web-search", "rag", "codebase", "knowledge-graph",
        "graphrag", "memory", "metasearch", "crawler", "mcp", "model-context-protocol"]):
        return "B"
    return "E"

TRACK = {
    "A": "① AI 网关 / 路由 / 成本压缩",
    "B": "② 代码上下文底座（MCP / 图谱 / 检索 / 记忆）",
    "C": "③ 技能层 / Skills / Prompt 工程",
    "D": "④ 编码 Agent 基座（终端 / CLI / Harness）",
    "E": "⑤ 全赛道热门 / 应用外溢（视频·量化·办公·平台）",
}
SHORT = {"A": "①网关", "B": "②上下文", "C": "③技能", "D": "④Agent", "E": "⑤外溢"}
REP = {
    "A": "OmniRoute",
    "B": "code-review-graph、wigolo、fastmcp",
    "C": "skills、agent-skills、hallmark、i-have-adhd",
    "D": "codex、openinterpreter、jcode、cline",
    "E": "OpenCut、Vibe-Trading、OfficeCLI",
}
ORDER = ["A", "B", "C", "D", "E"]

from collections import defaultdict
buckets = defaultdict(list)
for r in rows:
    buckets[classify(r)].append(r)
for k in buckets:
    buckets[k].sort(key=lambda x: -(int(x['stars']) if str(x['stars']).isdigit() else 0))

L = []
L.append("# GitHub AI 热门项目 · 全量知识库分类整理（2026-07-02 ~ 2026-07-22）")
L.append("")
L.append("> 归档范围：自动化执行第 1~20 次（2026-07-02 至 2026-07-22）")
L.append("> 内容：17 篇工作日 Vibe Coding 日报 + 3 篇周末全赛道周报 + 58 个项目页（去重后 %d 个唯一项目）" % N_UNIQUE)
L.append("> 数据源：GitHub Trending 飙升榜（?since=daily / ?since=weekly），按当日/当周新增 Star 降序")
L.append("> 本文件为「全部知识」的重新整理与分类，便于检索与沉淀。")
L.append("")
L.append("## 〇、赛道分类速览")
L.append("")
L.append("| 赛道 | 项目数 | 代表项目 |")
L.append("| --- | --- | --- |")
for k in ORDER:
    L.append("| %s | %d | %s |" % (TRACK[k], len(buckets.get(k, [])), REP.get(k, "")))
L.append("")
for k in ORDER:
    items = buckets.get(k, [])
    L.append("## %s（%d 个）" % (TRACK[k], len(items)))
    L.append("")
    L.append("| 项目 | 总 Star | 开源时间 | 标签 |")
    L.append("| --- | --- | --- | --- |")
    for r in items:
        L.append("| %s | %s | %s | %s |" % (r['alias'], r['stars'], r['created'], r['tags']))
    L.append("")

L.append("## 六、完整项目索引（%d 个唯一项目）" % N_UNIQUE)
L.append("")
L.append("| # | 项目 | 赛道 | 总 Star | 开源时间 |")
L.append("| --- | --- | --- | --- | --- |")
n = 0
allrows = sorted(rows, key=lambda x: -(int(x['stars']) if str(x['stars']).isdigit() else 0))
for r in allrows:
    n += 1
    L.append("| %d | %s | %s | %s | %s |" % (n, r['alias'], SHORT[classify(r)], r['stars'], r['created']))
L.append("")

L.append("## 七、每日 / 周 最佳项目（#1）演变时间线")
L.append("")
tl = [
    ("2026-07-02", "工作日", "cline / aider / continue / SWE-agent / gpt-engineer（初始种子库，无实时增量）"),
    ("2026-07-03", "工作日", "browser-use/video-use、affaan-m/ECC（按实时新增）"),
    ("2026-07-04", "周末", "OpenMontage（+10,199，全赛道周榜 #1）"),
    ("2026-07-05", "周末", "agency-agents（+10,976，全赛道周榜 #1）"),
    ("2026-07-06", "工作日", "system_prompts_leaks、claude-skills、planning-with-files"),
    ("2026-07-07", "工作日", "system_prompts_leaks、claude-skills"),
    ("2026-07-08", "工作日", "ai-job-search、system_prompts_leaks、agent-skills、claude-video、CodexBar"),
    ("2026-07-09", "工作日", "agent-skills、claude-video、CubeSandbox、TencentDB-Agent-Memory、last30days"),
    ("2026-07-10", "工作日", "ai-job-search、agent-skills、OfficeCLI、awesome-design-md、system_prompts_leaks"),
    ("2026-07-11", "工作日", "skills、OfficeCLI、agent-skills、superpowers、DesktopCommanderMCP"),
    ("2026-07-13", "工作日", "destructive_command_guard、claude-code-templates、hallmark、DesktopCommanderMCP、background-agents"),
    ("2026-07-14", "工作日", "graphify、hallmark、spec-kit、marketingskills、agent-skills"),
    ("2026-07-15", "工作日", "graphify、skills、Vibe-Trading、hallmark、dcg"),
    ("2026-07-16", "工作日", "skills、hallmark、Vibe-Trading、dcg、openinterpreter"),
    ("2026-07-17", "工作日", "hallmark、skills、graphify、openinterpreter、copilot-sdk"),
    ("2026-07-18", "工作日", "hallmark、openinterpreter、copilot-sdk、code-review-graph、cwc-workshops"),
    ("2026-07-19", "周末", "OpenCut（+12,718）、skills、graphify、hallmark、awesome-llm-apps、Vibe-Trading、orca、OfficeCLI、codex、openinterpreter"),
    ("2026-07-20", "工作日", "code-review-graph、wigolo、kimi-cli、jcode、copilot-sdk"),
    ("2026-07-21", "工作日", "code-review-graph、wigolo、kimi-cli、jcode、fastmcp"),
    ("2026-07-22", "工作日", "OmniRoute、code-review-graph、i-have-adhd、jcode、wigolo"),
]
L.append("| 日期 | 模式 | 今日/本周最佳（Top 项目） |")
L.append("| --- | --- | --- |")
for d, m, t in tl:
    L.append("| %s | %s | %s |" % (d, m, t))
L.append("")

L.append("## 八、跨期趋势总结")
L.append("")
L.append("1. **技能层（Skills）贯穿全程**：从首周 system_prompts_leaks / claude-skills，到中段 skills / agent-skills / graphify / hallmark / spec-kit，再到本周 i-have-adhd（输出风格），技能从「能力封装」演进到「交互风格封装」，是 Vibe Coding 最持久的主线。")
L.append("2. **代码上下文底座固化**：code-review-graph（图谱）+ wigolo（联网检索）自 07-20 起连续多日包揽工作日 #1/#2，标志竞争从「模型能力」下沉到「上下文工程基础设施」；fastmcp 作为 MCP 框架多次入榜，是底层协议底座。")
L.append("3. **编码 Agent 基座多元化**：codex / openinterpreter / SWE-agent / aider / cline / continue 等经典工具长期在榜；新兴 jcode（Rust）、kimi-cli（CLI）、copilot-sdk（官方 SDK 化）反映终端/CLI 编码 Agent 与「大厂标准化」并行。")
L.append("4. **AI 网关/路由成为新主线**：07-22 OmniRoute（免费 MIT 网关，统一接入 268+ 供应商、token 压缩 15–95%）登顶，标志 Vibe Coding 竞争进一步上移到「统一接入 + 成本压缩」层。")
L.append("5. **全赛道外溢（周末）**：视频创作（OpenCut）、量化交易（Vibe-Trading）、办公自动化（OfficeCLI）、LLM 应用平台（awesome-llm-apps / agency-agents）在周末榜持续出现，Agent 从写代码向创作/金融/办公扩散。")
L.append("")
L.append("## 九、关联归档")
L.append("")
L.append("- Obsidian 知识库：_Index.md（全局索引）+ Daily/（17 日报）+ Weekly/（3 周报）+ Projects/（58 文件 · 去重 %d 唯一）" % N_UNIQUE)
L.append("- 自动化执行日志：logs/task_2026-07-22.log 及历史 logs/task_YYYY-MM-DD.log")
L.append("- 本分类文档本地源：.workbuddy/tmp/ima_GitHub_AI_全量分类_2026-07-22.md")
L.append("")

out = "\n".join(L)
open('.workbuddy/tmp/ima_GitHub_AI_全量分类_2026-07-22.md', 'w', encoding='utf-8').write(out)
print("written bytes:", len(out.encode('utf-8')))
print("projects (after dedup):", len(rows), "| dropped duplicates:", deduped_from)
for k in ORDER:
    print("  %s: %d" % (TRACK[k], len(buckets.get(k, []))))
PY = None
