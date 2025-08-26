#!/usr/bin/env python3

import argparse
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, List, Optional, Sequence, Tuple


STEP_DIR_NAME_DEFAULT = "steps"
STEP_PREFIX = "step-"
STEP_DIR_PATTERN = re.compile(rf"^{re.escape(STEP_PREFIX)}(\d{{3}})$")


@dataclass
class SnapshotPlan:
    repository_root: Path
    steps_root: Path
    step_directory: Path
    step_name: str
    files_to_capture: List[Path]
    diffs_text: Optional[str]


def run_command(command: Sequence[str], cwd: Optional[Path] = None) -> Tuple[int, str, str]:
    process = subprocess.Popen(
        command,
        cwd=str(cwd) if cwd else None,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    stdout, stderr = process.communicate()
    return process.returncode, stdout, stderr


def detect_repository_root(explicit_root: Optional[str]) -> Path:
    if explicit_root:
        return Path(explicit_root).resolve()
    # Try to detect via git
    code, out, _ = run_command(["git", "rev-parse", "--show-toplevel"], cwd=Path.cwd())
    if code == 0:
        return Path(out.strip()).resolve()
    # Fallback to current working directory
    return Path.cwd().resolve()


def is_git_repository(path: Path) -> bool:
    code, _, _ = run_command(["git", "rev-parse", "--is-inside-work-tree"], cwd=path)
    return code == 0


def list_changed_files_via_git(repo_root: Path) -> List[Path]:
    # Prefer tracked changes; include new files (??)
    code, out, err = run_command(["git", "status", "--porcelain"], cwd=repo_root)
    if code != 0:
        raise RuntimeError(f"git status failed: {err.strip()}")
    files: List[Path] = []
    for line in out.splitlines():
        # Lines are of form: XY path
        if not line.strip():
            continue
        # Handle rename syntax: R  old -> new
        payload = line[3:]
        if " -> " in payload:
            path = payload.split(" -> ", 1)[1]
        else:
            path = payload
        candidate = (repo_root / path.strip()).resolve()
        if candidate.exists():
            files.append(candidate)
    return files


def normalize_files(files: Iterable[str], base: Path) -> List[Path]:
    normalized: List[Path] = []
    for f in files:
        candidate = (base / f).resolve() if not os.path.isabs(f) else Path(f).resolve()
        if not candidate.exists():
            raise FileNotFoundError(f"File does not exist: {candidate}")
        if not str(candidate).startswith(str(base)):
            raise ValueError(f"File must reside within repository root: {candidate}")
        normalized.append(candidate)
    return normalized


def ensure_steps_root(root: Path, steps_dir_name: str) -> Path:
    steps_root = (root / steps_dir_name).resolve()
    steps_root.mkdir(parents=True, exist_ok=True)
    return steps_root


def compute_next_step_name(steps_root: Path) -> str:
    max_index = 0
    if steps_root.exists():
        for child in steps_root.iterdir():
            if child.is_dir():
                match = STEP_DIR_PATTERN.match(child.name)
                if match:
                    index = int(match.group(1))
                    if index > max_index:
                        max_index = index
    next_index = max_index + 1
    return f"{STEP_PREFIX}{next_index:03d}"


def copy_files_to_step(step_dir: Path, repo_root: Path, files: Sequence[Path], steps_root: Path, dry_run: bool, verbose: bool) -> List[Path]:
    copied_files: List[Path] = []
    for absolute_path in files:
        # Skip files already under steps root to avoid recursion
        try:
            absolute_path.relative_to(steps_root)
            if verbose:
                print(f"[skip] Inside steps directory: {absolute_path}")
            continue
        except ValueError:
            pass
        rel_path = absolute_path.relative_to(repo_root)
        destination = step_dir / rel_path
        if verbose or dry_run:
            print(f"[copy] {rel_path} -> {destination}")
        if not dry_run:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(absolute_path, destination)
        copied_files.append(rel_path)
    return copied_files


def gather_git_diff(repo_root: Path, files: Sequence[Path], max_lines: int, context: int, compare_to: Optional[str]) -> str:
    # Build diff command
    base_cmd = ["git", "diff", "--no-ext-diff", "--no-color", f"-U{context}"]
    if compare_to:
        base_cmd.append(compare_to)
    # Append files relative paths
    rel_paths = [str(p.relative_to(repo_root)) for p in files]
    cmd = base_cmd + ["--", *rel_paths]
    code, out, err = run_command(cmd, cwd=repo_root)
    if code != 0:
        raise RuntimeError(f"git diff failed: {err.strip()}")
    lines = out.splitlines()
    if max_lines > 0 and len(lines) > max_lines:
        truncated = lines[:max_lines] + [f"... (truncated, total {len(lines)} lines)"]
        return "\n".join(truncated)
    return out


def build_markdown_section(step_name: str, files: Sequence[Path], custom_message: Optional[str], include_diff: bool, diff_text: Optional[str]) -> str:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines: List[str] = []
    lines.append(f"## {step_name} - {timestamp}")
    lines.append("### Files")
    for rel in files:
        lines.append(f"- {rel.as_posix()}")
    lines.append("")
    lines.append("### Diff")
    if custom_message:
        lines.append(f"- {custom_message}")
    if include_diff and diff_text:
        lines.append("```")
        # Use plain fenced code block to keep file small/portable.
        lines.append(diff_text.rstrip())
        lines.append("```")
    else:
        lines.append("- 差分は省略されています。必要に応じて `--include-diff` で出力できます。")
    lines.append("")
    return "\n".join(lines)


def append_to_step_diffs(repo_root: Path, section_text: str, dry_run: bool, verbose: bool) -> Path:
    diffs_file = (repo_root / "STEP_DIFFS.md").resolve()
    if verbose or dry_run:
        print(f"[append] {diffs_file}")
    if not dry_run:
        with diffs_file.open("a", encoding="utf-8") as f:
            if diffs_file.stat().st_size > 0:
                f.write("\n")
            f.write(section_text)
            f.write("\n")
    return diffs_file


def plan_snapshot(
    explicit_root: Optional[str],
    steps_dir_name: str,
    use_git: Optional[bool],
    provided_files: Optional[List[str]],
    include_diff: bool,
    diff_context: int,
    max_diff_lines: int,
    diff_compare_to: Optional[str],
    message: Optional[str],
    dry_run: bool,
    verbose: bool,
) -> SnapshotPlan:
    repo_root = detect_repository_root(explicit_root)
    repo_root = repo_root.resolve()

    git_repo = is_git_repository(repo_root)
    if use_git is False:
        git_repo = False
    elif use_git is True:
        if not git_repo:
            raise RuntimeError("--git was specified but this is not a git repository")

    if provided_files:
        files = normalize_files(provided_files, base=repo_root)
    else:
        if git_repo:
            files = list_changed_files_via_git(repo_root)
        else:
            raise ValueError("No files specified and git is unavailable. Provide --files or run inside a git repository.")

    if not files:
        raise ValueError("No target files were found to snapshot.")

    steps_root = ensure_steps_root(repo_root, steps_dir_name)
    step_name = compute_next_step_name(steps_root)
    step_dir = steps_root / step_name
    if not dry_run:
        step_dir.mkdir(parents=True, exist_ok=True)

    copied_rel_paths = copy_files_to_step(step_dir, repo_root, files, steps_root, dry_run, verbose)

    diffs_text: Optional[str] = None
    if include_diff and git_repo:
        diffs_text = gather_git_diff(
            repo_root=repo_root,
            files=files,
            max_lines=max_diff_lines,
            context=diff_context,
            compare_to=diff_compare_to,
        )

    return SnapshotPlan(
        repository_root=repo_root,
        steps_root=steps_root,
        step_directory=step_dir,
        step_name=step_name,
        files_to_capture=copied_rel_paths,
        diffs_text=diffs_text,
    )


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Save a snapshot of current work files into steps/step-XXX and append an entry to STEP_DIFFS.md"
        )
    )
    parser.add_argument("--root", dest="root", default=None, help="Repository root (defaults to git root or CWD)")
    parser.add_argument(
        "--steps-dir",
        dest="steps_dir",
        default=STEP_DIR_NAME_DEFAULT,
        help=f"Steps directory name relative to root (default: {STEP_DIR_NAME_DEFAULT})",
    )
    parser.add_argument("--files", nargs="*", default=None, help="Explicit file paths to include (relative to root or absolute)")
    parser.add_argument("--git", dest="use_git", action="store_true", help="Force using git to detect changes")
    parser.add_argument("--no-git", dest="no_git", action="store_true", help="Disable git even if available")
    parser.add_argument("--include-diff", action="store_true", help="Include git diff output in STEP_DIFFS.md")
    parser.add_argument("--diff-context", type=int, default=3, help="Number of context lines for git diff (default: 3)")
    parser.add_argument(
        "--max-diff-lines",
        type=int,
        default=800,
        help="Maximum lines of diff to include before truncation (default: 800, 0 = unlimited)",
    )
    parser.add_argument(
        "--diff-compare-to",
        dest="diff_compare_to",
        default=None,
        help="Optional git ref to compare against (e.g., HEAD). If omitted, compares working tree",
    )
    parser.add_argument("--message", default=None, help="Additional note to include under the Diff section")
    parser.add_argument("--dry-run", action="store_true", help="Do not write files; show what would happen")
    parser.add_argument("--verbose", action="store_true", help="Print detailed logging")

    args = parser.parse_args(argv)

    use_git: Optional[bool]
    if args.no_git:
        use_git = False
    elif args.use_git:
        use_git = True
    else:
        use_git = None

    try:
        plan = plan_snapshot(
            explicit_root=args.root,
            steps_dir_name=args.steps_dir,
            use_git=use_git,
            provided_files=args.files if args.files else None,
            include_diff=args.include_diff,
            diff_context=args.diff_context,
            max_diff_lines=args.max_diff_lines,
            diff_compare_to=args.diff_compare_to,
            message=args.message,
            dry_run=args.dry_run,
            verbose=args.verbose,
        )

        section_text = build_markdown_section(
            step_name=plan.step_name,
            files=plan.files_to_capture,
            custom_message=args.message,
            include_diff=args.include_diff,
            diff_text=plan.diffs_text,
        )

        diffs_path = append_to_step_diffs(plan.repository_root, section_text, dry_run=args.dry_run, verbose=args.verbose)

        print(
            f"Created {plan.step_name} at {plan.step_directory} and appended to {diffs_path}"
            + (" (dry run)" if args.dry_run else "")
        )
        return 0
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())