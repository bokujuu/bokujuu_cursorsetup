# -*- coding: utf-8 -*-
"""Validate new global skills and templates for bokujuu_cursorsetup."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
errors: list[str] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    if ok:
        print(f"[OK] {name}" + (f" - {detail}" if detail else ""))
    else:
        errors.append(f"{name}: {detail}")
        print(f"[FAIL] {name} - {detail}")


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
        lines = [
            ln.strip()
            for ln in desc_m.group(1).splitlines()
            if ln.strip()
        ]
        out["description"] = " ".join(lines)
    else:
        desc_one = re.search(r"^description:\s*(.+)$", block, re.M)
        if desc_one:
            out["description"] = desc_one.group(1).strip().strip("'\"")
    return out


def main() -> int:
    skills = [
        "skill-lifecycle",
        "system-structure-viz",
        "context-engineering",
        "harness-engineering",
    ]
    for slug in skills:
        skill_md = ROOT / "skills" / slug / "SKILL.md"
        ref_md = ROOT / "skills" / slug / "reference.md"
        check(f"{slug}/SKILL.md exists", skill_md.is_file())
        check(f"{slug}/reference.md exists", ref_md.is_file())
        fm = parse_frontmatter(skill_md)
        check(f"{slug} frontmatter name", fm.get("name") == slug, repr(fm.get("name")))
        desc = fm.get("description", "")
        check(f"{slug} description length", len(desc) >= 80, f"len={len(desc)}")
        check(f"{slug} description has 'not for'", "not for" in desc.lower() or "not for" in desc)

    registry = ROOT / "templates/project-skills/practice-registry.json"
    data = json.loads(registry.read_text(encoding="utf-8"))
    check("practice-registry.json", data.get("version") == 1)
    check("registry practices array", isinstance(data.get("practices"), list))

    paths_must_exist = [
        "templates/project-skills/README.md",
        "templates/project-skills/skill/SKILL.md",
        "templates/project-skills/skill/references/skill-memory.md",
        "templates/structure-viz/README.md",
        "templates/structure-viz/architecture.md",
        "templates/structure-viz/site/index.html",
        "docs/references/muse-autoskill.md",
        "docs/pr/009-skill-lifecycle-structure-viz.md",
        "docs/pr/012-context-engineering-harness-engineering.md",
    ]
    for rel in paths_must_exist:
        check(rel, (ROOT / rel).is_file())

    sl = parse_frontmatter(ROOT / "skills/skill-lifecycle/SKILL.md")["description"]
    iwp = parse_frontmatter(ROOT / "skills/implement-with-practices/SKILL.md")["description"]
    overlap_phrases = ["library", "framework", "api"]
    sl_lower, iwp_lower = sl.lower(), iwp.lower()
    check(
        "description boundary (skill-lifecycle mentions task-category)",
        "task" in sl_lower or "workflow" in sl_lower or "recurring" in sl_lower,
    )
    check(
        "description boundary (implement-with-practices is tech-specific)",
        "library" in iwp_lower or "framework" in iwp_lower or "api" in iwp_lower,
    )

    html = (ROOT / "templates/structure-viz/site/index.html").read_text(encoding="utf-8")
    check("structure-viz HTML has mermaid", "mermaid" in html.lower())
    check("structure-viz HTML no fetch", "fetch(" not in html)

    arch = (ROOT / "templates/structure-viz/architecture.md").read_text(encoding="utf-8")
    check("architecture.md has mermaid blocks", arch.count("```mermaid") >= 2)

    install_ps1 = (ROOT / "scripts/install.ps1").read_text(encoding="utf-8")
    check(
        "install.ps1 Root is one level up from scripts",
        'Split-Path -Parent $PSScriptRoot' in install_ps1
        and "Split-Path -Parent (Split-Path -Parent" not in install_ps1,
    )

    codex = Path.home() / ".codex" / "skills"
    for slug in skills:
        check(f"installed {slug}", (codex / slug / "SKILL.md").is_file())

    japanese_skills: dict[str, list[str]] = {
        "japanese-doc-review": [
            "references/01-structure.md",
            "references/02-grammar.md",
            "references/03-style.md",
            "references/04-typo.md",
            "references/review-result-format.md",
            "references/sources.md",
            "references/skill-memory.md",
        ],
        "japanese-technical-writing": [
            "references/00-template-policy.md",
            "references/01-structure.md",
            "references/02-grammar.md",
            "references/03-style.md",
            "references/templates/design-doc.md",
            "references/templates/explanation.md",
            "references/templates/howto.md",
            "references/templates/incident-report.md",
            "references/templates/investigation-report.md",
            "references/sources.md",
            "references/skill-memory.md",
            "agents/openai.yaml",
        ],
    }
    for slug, rel_paths in japanese_skills.items():
        skill_dir = ROOT / "skills" / slug
        skill_md = skill_dir / "SKILL.md"
        check(f"{slug}/SKILL.md exists", skill_md.is_file())
        line_count = len(skill_md.read_text(encoding="utf-8").splitlines()) if skill_md.is_file() else 0
        check(f"{slug} SKILL.md line count", line_count <= 500, f"lines={line_count}")
        fm = parse_frontmatter(skill_md)
        check(f"{slug} frontmatter name", fm.get("name") == slug, repr(fm.get("name")))
        desc = fm.get("description", "")
        check(f"{slug} description non-empty", len(desc) >= 20, f"len={len(desc)}")
        for rel in rel_paths:
            check(f"{slug}/{rel} exists", (skill_dir / rel).is_file())
        sources = skill_dir / "references" / "sources.md"
        if sources.is_file():
            src_text = sources.read_text(encoding="utf-8")
            check(
                f"{slug} sources.md has upstream URL",
                "himadajin/skills" in src_text,
            )
        check(f"installed {slug}", (codex / slug / "SKILL.md").is_file())

    return 1 if errors else 0


if __name__ == "__main__":
    rc = main()
    if errors:
        print("\nErrors:")
        for e in errors:
            print(f"  - {e}")
    sys.exit(rc)
