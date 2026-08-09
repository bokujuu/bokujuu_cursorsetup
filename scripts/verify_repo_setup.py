# -*- coding: utf-8 -*-
"""bokujuu_cursorsetup のエージェント基盤・skills 同梱を機械検証する。"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
MANIFEST = REPO_ROOT / "MANIFEST.md"
AGENTS = REPO_ROOT / "AGENTS.md"
REGISTRY = REPO_ROOT / ".codex" / "practice-registry.json"
INSTALL_PS1 = REPO_ROOT / "scripts" / "install.ps1"
INSTALL_SH = REPO_ROOT / "scripts" / "install.sh"

REQUIRED_TEMPLATE_PATHS = [
    "templates/project-skills/README.md",
    "templates/project-skills/practice-registry.json",
    "templates/project-skills/skill/SKILL.md",
    "templates/project-skills/skill/references/skill-memory.md",
    "templates/structure-viz/README.md",
    "templates/structure-viz/architecture.md",
    "templates/structure-viz/site/index.html",
    "templates/loop-orchestration/README.md",
]


def fail(messages: list[str]) -> int:
    for msg in messages:
        print(f"[FAIL] {msg}", file=sys.stderr)
    return 1


def ok(message: str) -> None:
    print(f"[OK] {message}")


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    end = text.find("---", 3)
    if end < 0:
        return {}
    block = text[3:end]
    out: dict[str, str] = {}
    name_m = re.search(r"^name:\s*(.+)$", block, re.M)
    if name_m:
        out["name"] = name_m.group(1).strip()
    desc_m = re.search(
        r"^description:\s*>-\s*\n((?:[ \t].+\n?)+)",
        block,
        re.M,
    )
    if desc_m:
        lines = [ln.strip() for ln in desc_m.group(1).splitlines() if ln.strip()]
        out["description"] = " ".join(lines)
    else:
        desc_one = re.search(r"^description:\s*(.+)$", block, re.M)
        if desc_one:
            out["description"] = desc_one.group(1).strip().strip("'\"")
    return out


def verify_agents_and_registry(errors: list[str]) -> None:
    if not AGENTS.is_file():
        errors.append("Missing AGENTS.md at repo root")
    else:
        ok("AGENTS.md present")

    if not REGISTRY.is_file():
        errors.append("Missing .codex/practice-registry.json")
        return

    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    if data.get("version") != 1:
        errors.append("practice-registry.json: version must be 1")
    practices = data.get("practices")
    if not isinstance(practices, list) or not practices:
        errors.append("practice-registry.json: practices must be a non-empty list")
        return

    ok("practice-registry.json valid")
    for entry in practices:
        slug = entry.get("slug", "")
        rel = str(entry.get("skill_path", "")).strip()
        skill_path = (REPO_ROOT / rel).resolve()
        if not skill_path.is_file():
            errors.append(f"registry skill_path missing: {rel}")
        else:
            ok(f"registry skill_path: {slug}")


def verify_skills_manifest(errors: list[str]) -> None:
    if not SKILLS_DIR.is_dir():
        errors.append(f"Missing skills directory: {SKILLS_DIR}")
        return

    if not MANIFEST.is_file():
        errors.append("Missing MANIFEST.md")
        return

    manifest_text = MANIFEST.read_text(encoding="utf-8")
    skill_dirs = sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir())

    for skill_dir in skill_dirs:
        slug = skill_dir.name
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.is_file():
            errors.append(f"Missing SKILL.md: skills/{slug}/SKILL.md")
            continue

        fm = parse_frontmatter(skill_md)
        if fm.get("name") != slug:
            errors.append(
                f"skills/{slug}: frontmatter name={fm.get('name')!r} != folder name"
            )
        else:
            ok(f"skill frontmatter name: {slug}")

        if slug not in manifest_text:
            errors.append(f"MANIFEST.md does not mention skill: {slug}")
        else:
            ok(f"MANIFEST mentions: {slug}")

        desc = fm.get("description", "")
        if len(desc) < 20:
            errors.append(f"skills/{slug}: description too short (len={len(desc)})")


def verify_install_ps1(errors: list[str]) -> None:
    if not INSTALL_PS1.is_file():
        errors.append("Missing scripts/install.ps1")
        return
    text = INSTALL_PS1.read_text(encoding="utf-8")
    if "Split-Path -Parent $PSScriptRoot" not in text:
        errors.append("install.ps1: expected Split-Path -Parent $PSScriptRoot")
    if "Split-Path -Parent (Split-Path -Parent" in text:
        errors.append("install.ps1: must not use double Split-Path for Root")
    else:
        ok("install.ps1 Root path pattern")


def verify_codex_mcp_installers(errors: list[str]) -> None:
    if not INSTALL_PS1.is_file():
        return

    powershell_text = INSTALL_PS1.read_text(encoding="utf-8")
    for marker in ("InstallCodexMcp", "CodexFilesystemRoot", "codex mcp add"):
        if marker not in powershell_text:
            errors.append(f"install.ps1: missing Codex MCP marker: {marker}")
    if all(marker in powershell_text for marker in ("InstallCodexMcp", "codex mcp add")):
        ok("install.ps1 Codex MCP registration")

    if not INSTALL_SH.is_file():
        errors.append("Missing scripts/install.sh")
        return

    shell_text = INSTALL_SH.read_text(encoding="utf-8")
    for marker in ("--install-codex-mcp", "--codex-filesystem-root", "codex mcp add"):
        if marker not in shell_text:
            errors.append(f"install.sh: missing Codex MCP marker: {marker}")
    if all(marker in shell_text for marker in ("--install-codex-mcp", "codex mcp add")):
        ok("install.sh Codex MCP registration")


def verify_templates(errors: list[str]) -> None:
    for rel in REQUIRED_TEMPLATE_PATHS:
        path = REPO_ROOT / rel
        if not path.is_file():
            errors.append(f"Missing template path: {rel}")
        else:
            ok(f"template: {rel}")


def verify_installed_skills(errors: list[str], *, repo_only: bool) -> None:
    if repo_only:
        ok("installed skills check skipped (--repo-only)")
        return

    if not SKILLS_DIR.is_dir():
        return

    codex_skills = Path.home() / ".codex" / "skills"
    for skill_dir in sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir()):
        slug = skill_dir.name
        installed = codex_skills / slug / "SKILL.md"
        if not installed.is_file():
            errors.append(
                f"installed skill missing: ~/.codex/skills/{slug}/SKILL.md "
                "(run scripts/install.ps1 or scripts/install.sh first)"
            )
        else:
            ok(f"installed: {slug}")


def verify_loop_kit_subprocess(errors: list[str]) -> None:
    script = REPO_ROOT / "scripts" / "verify_loop_kit.py"
    if not script.is_file():
        errors.append("Missing scripts/verify_loop_kit.py")
        return
    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )
    if result.returncode != 0:
        errors.append("verify_loop_kit.py failed")
        if result.stderr:
            errors.append(result.stderr.strip()[:500])
    else:
        ok("verify_loop_kit.py passed")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verify bokujuu_cursorsetup agent bootstrap and skill distribution.",
    )
    parser.add_argument(
        "--repo-only",
        action="store_true",
        help="Skip ~/.codex/skills/ install checks (repo file integrity only).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    errors: list[str] = []

    verify_agents_and_registry(errors)
    verify_skills_manifest(errors)
    verify_install_ps1(errors)
    verify_codex_mcp_installers(errors)
    verify_templates(errors)
    verify_installed_skills(errors, repo_only=args.repo_only)
    verify_loop_kit_subprocess(errors)

    if errors:
        return fail(errors)

    print("verify_repo_setup: all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
