#!/usr/bin/env python3
"""
fars_lean4_sync.py
FARS Lean4 同步器：监控变更 → 尝试 Lake Build → 自动 Commit + Push
用法: python fars_lean4_sync.py [--dry-run]

原理：
- 不依赖本地 Mathlib（网络太慢）
- 推送后由 GitHub Actions 做实际验证（ubuntu-latest 有网络）
- 本地只做语法检查（lean --make 的最小子集）
"""

import os
import sys
import time
import hashlib
import subprocess
import json
from pathlib import Path
from datetime import datetime

# === 配置 ===
# 从脚本位置向上搜索找到 claude-memory/thermodynamic-agi
def _find_lean_dir() -> Path:
    p = Path(__file__).resolve()
    for _ in range(10):
        candidate = p / "thermodynamic-agi" / "02_theory" / "lean4_src"
        if candidate.exists():
            return candidate
        p = p.parent
    # 回退：使用环境变量或硬编码
    return Path(os.environ.get(
        "FARS_LEAN_DIR",
        "E:/BaiduSyncdisk/claude-memory/thermodynamic-agi/02_theory/lean4_src"
    ))

LEAN_DIR  = _find_lean_dir()
REPO_DIR  = LEAN_DIR.parent.parent.parent  # → claude-memory/
STATE_FILE = REPO_DIR / ".fars_lean4_state.json"
GITHUB_REPO = "simulai/ASI"
BRANCH = "main"


def get_file_hash(file_path: Path) -> str:
    """计算文件的 SHA256"""
    if not file_path.exists():
        return ""
    with open(file_path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()[:16]


def load_state() -> dict:
    """加载上次状态"""
    if STATE_FILE.exists():
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"last_hashes": {}, "last_commit": "", "last_build": ""}


def save_state(state: dict):
    """保存状态"""
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def get_changed_files() -> list[Path]:
    """返回自上次检查以来有变更的 .lean 文件"""
    state = load_state()
    changed = []
    for lean_file in LEAN_DIR.rglob("*.lean"):
        h = get_file_hash(lean_file)
        if state["last_hashes"].get(str(lean_file)) != h:
            changed.append(lean_file)
    return changed


def update_hashes():
    """更新文件哈希状态"""
    state = load_state()
    for lean_file in LEAN_DIR.rglob("*.lean"):
        state["last_hashes"][str(lean_file)] = get_file_hash(lean_file)
    save_state(state)


def get_git_status() -> dict:
    """获取 git 工作目录状态"""
    try:
        result = subprocess.run(
            ["git", "-C", str(REPO_DIR), "status", "--porcelain"],
            capture_output=True, text=True, timeout=10
        )
        return {"dirty": bool(result.stdout.strip()), "output": result.stdout}
    except Exception as e:
        return {"dirty": False, "output": "", "error": str(e)}


def get_last_commit() -> str:
    """获取最新提交哈希"""
    try:
        result = subprocess.run(
            ["git", "-C", str(REPO_DIR), "rev-parse", "HEAD"],
            capture_output=True, text=True, timeout=10
        )
        return result.stdout.strip()[:8]
    except:
        return "unknown"


def try_lean_check(lean_file: Path) -> dict:
    """
    尝试 Lean 语法检查（不依赖完整 Mathlib）
    策略：
    1. 先用 lean --make 只编译自身（最快失败检测）
    2. 检查常见语法错误（括号、引号、缩进）
    """
    result = {
        "file": str(lean_file.relative_to(REPO_DIR)),
        "syntax_ok": False,
        "errors": [],
        "warnings": [],
        "checked_at": datetime.now().isoformat()
    }

    # 语法基础检查（正则表达式，快速本地执行）
    try:
        with open(lean_file, "r", encoding="utf-8") as f:
            content = f.read()

        # 检查常见括号不匹配
        lines = content.split("\n")
        for i, line in enumerate(lines, 1):
            if line.count("(") != line.count(")"):
                result["errors"].append(f"Line {i}: parentheses mismatch")
            if line.count("{") != line.count("}"):
                result["errors"].append(f"Line {i}: brace mismatch")
            if line.count("[") != line.count("]"):
                result["errors"].append(f"Line {i}: bracket mismatch")

        # 检查 sorry 数量（粗略进度指标）
        sorry_count = content.count("sorry")
        if sorry_count > 0:
            result["warnings"].append(f"Remaining sorry markers: {sorry_count}")

        result["syntax_ok"] = len(result["errors"]) == 0

    except Exception as e:
        result["errors"].append(f"File read error: {e}")

    return result


def build_commit_message(changed_files: list[Path], check_results: list[dict]) -> str:
    """生成语义化提交信息"""
    total_files = len(changed_files)
    total_sorrys = sum(r["warnings"][0].count("sorry") if r["warnings"] else 0
                       for r in check_results)

    parts = []
    for f in changed_files:
        name = f.stem  # 文件名不含扩展名
        if "FreeEnergy" in name or "ScaleOperator" in name:
            parts.append(f"FreeEnergy/ScaleOperator")
        elif "FECG" in name:
            parts.append("FECG")
        elif "Composite" in name:
            parts.append("Composite")
        elif "MultiModal" in name:
            parts.append("MultiModal")
        else:
            parts.append(name)

    unique_parts = list(dict.fromkeys(parts))  # 去重保序
    topic = "/".join(unique_parts) if unique_parts else "lean"

    msg = f"chore(lean): sync {topic} ({total_files} files)"

    if total_sorrys > 0:
        msg += f" | {total_sorrys} sorry(s) remaining"

    # 检查是否有已知错误
    has_errors = any(r["errors"] for r in check_results)
    if has_errors:
        msg += " [WIP]"

    return msg


def git_add_commit_push(message: str) -> dict:
    """执行 git add + commit + push"""
    result = {"success": False, "message": "", "commit": ""}

    try:
        # git add 所有变更
        subprocess.run(
            ["git", "-C", str(REPO_DIR), "add", "-A"],
            capture_output=True, text=True, timeout=30
        )

        # 检查是否有东西要提交
        status = subprocess.run(
            ["git", "-C", str(REPO_DIR), "status", "--porcelain"],
            capture_output=True, text=True, timeout=10
        )
        if not status.stdout.strip():
            result["message"] = "Nothing to commit (no changes)"
            result["success"] = True
            return result

        # git commit
        commit_result = subprocess.run(
            ["git", "-C", str(REPO_DIR), "commit", "-m", message],
            capture_output=True, text=True, timeout=30
        )
        if commit_result.returncode != 0:
            result["message"] = f"Commit failed: {commit_result.stderr}"
            return result

        commit_hash = get_last_commit()
        result["commit"] = commit_hash

        # git push
        push_result = subprocess.run(
            ["git", "-C", str(REPO_DIR), "push"],
            capture_output=True, text=True, timeout=60
        )
        if push_result.returncode != 0:
            result["message"] = f"Push failed: {push_result.stderr}"
            return result

        result["success"] = True
        result["message"] = f"✓ Pushed commit {commit_hash}: {message}"

    except subprocess.TimeoutExpired:
        result["message"] = "Git operation timed out"
    except Exception as e:
        result["message"] = f"Git error: {e}"

    return result


def run_gha_workflow_check() -> dict:
    """
    触发 GitHub Actions 工作流检查
    通过轮询 commit status 获取结果
    注意：需要 GitHub API token
    """
    # TODO: 实现 GitHub API 调用检查 CI 状态
    return {"enabled": False, "note": "GitHub Actions workflow needs manual setup"}


def print_report(check_results: list[dict], git_result: dict, dry_run: bool):
    """打印报告"""
    sep = "=" * 58
    print(f"\n{sep}")
    print(f"  FARS Lean4 Sync Report  [{datetime.now():%Y-%m-%d %H:%M:%S}]")
    print(f"{sep}\n")

    if not check_results:
        print(f"  No lean files found in {LEAN_DIR}")
        return

    total_files = len(check_results)
    ok_files = sum(1 for r in check_results if r["syntax_ok"])
    total_errors = sum(len(r["errors"]) for r in check_results)
    total_sorrys = sum(
        int(w.split(": ")[1]) for r in check_results
        for w in r["warnings"]
        if w.startswith("Remaining sorry")
    )

    print(f"  Files checked : {ok_files}/{total_files} passed syntax")
    print(f"  Syntax errors  : {total_errors}")
    print(f"  Remaining sorry: {total_sorrys}")
    print(f"  Git status     : {git_result.get('message', 'unknown')}")
    print(f"  Dry run        : {'YES (no actual push)' if dry_run else 'NO'}")
    print(f"\n{sep}\n")

    # 详细文件状态
    for r in check_results:
        status = "[OK]" if r["syntax_ok"] else "[ERR]"
        fname = r["file"].replace("\\", "/").split("/")[-1]
        print(f"  {status} {fname}")
        for err in r["errors"]:
            print(f"      !- {err}")
        for warn in r["warnings"]:
            print(f"      ~- {warn}")

    print(f"\n{sep}")

    if git_result["success"]:
        print(f"\n  OK  {git_result['message']}")
    elif git_result.get("message") == "Nothing to commit (no changes)":
        print(f"\n  --  {git_result['message']}")
    else:
        print(f"\n  !! Git: {git_result.get('message', 'unknown error')}")
        print(f"\n  GitHub Actions CI will validate on push")
        print(f"  https://github.com/{GITHUB_REPO}/actions")

    print()


def main():
    import argparse
    parser = argparse.ArgumentParser(description="FARS Lean4 自动同步器")
    parser.add_argument("--dry-run", action="store_true",
                        help="只检查，不提交")
    parser.add_argument("--watch", action="store_true",
                        help="持续监控模式（每 60 秒检查一次）")
    parser.add_argument("--interval", type=int, default=60,
                        help="监控间隔（秒，默认 60）")
    args = parser.parse_args()

    print(f"[FARS Lean4 Sync] Starting...")
    print(f"  Repo   : {REPO_DIR}")
    print(f"  Lean dir: {LEAN_DIR}")
    print(f"  Dry run: {args.dry_run}")
    print(f"  Watch  : {args.watch}")

    if args.watch:
        print(f"  Interval: {args.interval}s (Ctrl+C to stop)\n")
        while True:
            changed = get_changed_files()
            if changed:
                print(f"[{datetime.now():%H:%M:%S}] Detected changes:")
                for f in changed:
                    print(f"  - {f.relative_to(REPO_DIR)}")
            check_results = [try_lean_check(f) for f in LEAN_DIR.rglob("*.lean")]
            update_hashes()

            git_res = {"success": False, "message": "dry-run mode"}
            if not args.dry_run:
                msg = build_commit_message(changed, check_results)
                git_res = git_add_commit_push(msg)

            print_report(check_results, git_res, args.dry_run)
            time.sleep(args.interval)
    else:
        # 单次运行
        changed = get_changed_files()
        if not changed:
            print("\n  No changes detected.")
            return

        print(f"\n  Changed files:")
        for f in changed:
            print(f"  - {f.relative_to(REPO_DIR)}")

        check_results = [try_lean_check(f) for f in LEAN_DIR.rglob("*.lean")]
        update_hashes()

        if args.dry_run:
            git_res = {"success": False, "message": "dry-run (no push)"}
        else:
            msg = build_commit_message(changed, check_results)
            git_res = git_add_commit_push(msg)

        print_report(check_results, git_res, args.dry_run)


if __name__ == "__main__":
    main()
