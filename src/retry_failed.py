#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""回填重试：对指定日期的日报，重处理其中 clone 失败的仓库。

- 克隆到新目录（<owner>__<name>_retry），不触碰原有 clones/ 下可能存在的半截目录。
- 成功后重新检测构建系统 / 安装 / 冒烟 / 评分，更新元数据并整体重写日报。
- 日报头部的「扫描数 / AI 过滤后」从原报告解析保留，避免数字失真。

用法：python src/retry_failed.py 2026-07-29 2026-07-30
"""
import os
import sys
import json
import re
import time
import shutil
import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import main as _main
from main import (
    log, run_cmd, detect_build, install_project, smoke_run,
    score_project, write_report, CLONES_DIR,
)

CLONE_TIMEOUT = int(os.environ.get("CLONE_TIMEOUT", "300"))


def retry_date(date_str: str):
    ROOT = Path(__file__).resolve().parent.parent
    DAILY_DIR = ROOT / "reports" / "daily"
    META_DIR = ROOT / "data" / "metadata"
    date = datetime.date.fromisoformat(date_str)
    md_path = DAILY_DIR / f"{date_str}.md"
    meta_path = META_DIR / f"{date_str}.json"
    if not md_path.exists() or not meta_path.exists():
        log(f"跳过 {date_str}：缺少报告或元数据文件")
        return

    text = md_path.read_text(encoding="utf-8")
    m = re.search(r"扫描数\*\*：(\d+).*?AI 过滤后\*\*：(\d+)", text, re.S)
    scanned = int(m.group(1)) if m else len(results)
    filtered = int(m.group(2)) if m else len(results)

    results = json.loads(meta_path.read_text(encoding="utf-8"))
    changed = False
    for r in results:
        if r.get("clone") is True:
            continue
        p = r["project"]
        log(f"--- 重试克隆 {p['full']} ---")
        # 用带时间戳的唯一目录名，避免与可能存在的锁定/半截目录冲突（不删除任何已有目录）。
        safe = f"{p['owner']}__{p['name']}_retry_{int(time.time()*1000)}"
        dest = CLONES_DIR / safe
        t0 = time.time()
        rc, out, err = 1, "", "not attempted"
        last_err = ""
        # 大仓库直连易在初始 pack 传输被重置：用 blobless 浅克隆缩小初始流量，
        # 并切换 HTTP/1.1，最多 5 次退避重试覆盖瞬时抖动。
        for attempt in range(1, 6):
            rc, out, err = run_cmd(
                ["git", "-c", "http.version=HTTP/1.1", "-c", "http.postBuffer=524288000",
                 "clone", "--depth", str(_main.CLONE_DEPTH), "--filter=blob:none",
                 f"https://github.com/{p['full']}.git", str(dest)],
                timeout=CLONE_TIMEOUT,
            )
            if rc == 0:
                break
            last_err = err
            if attempt < 5:
                wait = 15 * attempt
                log(f"  ⚠️ 克隆第{attempt}次失败（{err[:120]}），{wait}s 后重试...")
                time.sleep(wait)
        err = last_err if rc != 0 else ""
        dt = round(time.time() - t0, 1)
        if rc == 0:
            r["clone"] = True
            r["clone_time"] = dt
            r["clone_err"] = ""
            build = detect_build(str(dest))
            istatus, ilog, it = install_project(p, str(dest), build)
            rstatus, rlog, rt = smoke_run(p, str(dest), build)
            score, stars = score_project(p, istatus, rstatus)
            r["build"] = build
            r["install"] = istatus
            r["install_log"] = ilog
            r["install_time"] = it
            r["run"] = rstatus
            r["run_log"] = rlog
            r["run_time"] = rt
            r["score"] = score
            r["stars"] = stars
            changed = True
            log(f"  ✅ {p['full']}（{dt}s）install={istatus} run={rstatus} score={score}")
        else:
            r["clone_err"] = err[:200]
            log(f"  ❌ 仍失败 {p['full']}: {err[:200]}")

    top = [r["project"] for r in results]
    if changed:
        write_report(date, top, results, scanned, filtered)
        meta_path.write_text(
            json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
        log(f"已重写 {date_str} 报告与元数据")
    else:
        log(f"{date_str} 无需变更")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python src/retry_failed.py YYYY-MM-DD [YYYY-MM-DD ...]")
        sys.exit(1)
    for d in sys.argv[1:]:
        retry_date(d)
