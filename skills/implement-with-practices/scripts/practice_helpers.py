from __future__ import annotations

import json
import re
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_RELATIVE_PATH = Path(".codex") / "practice-registry.json"
LOCAL_SKILLS_ROOT = Path(".codex") / "skills"
SNIPPET_ROOT = Path(".codex") / "practice-snippets"
STATUS_VALUES = {"draft", "approved"}
REQUIRED_FIELDS = [
    "slug",
    "summary",
    "trigger_keywords",
    "verification_commands",
    "source_urls",
    "skill_path",
    "status",
]
SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def normalize_lines(values: list[str]) -> list[str]:
    items: list[str] = []
    seen: set[str] = set()
    for value in values:
        stripped = value.strip()
        if not stripped or stripped in seen:
            continue
        seen.add(stripped)
        items.append(stripped)
    return items


def title_from_slug(slug: str) -> str:
    return " ".join(part.capitalize() for part in slug.split("-"))


def validate_slug(slug: str) -> bool:
    return len(slug) < 64 and bool(SLUG_PATTERN.fullmatch(slug))


def default_registry() -> dict:
    return {
        "version": "2026.03",
        "entries": [],
    }


def load_registry(target_root: Path) -> tuple[Path, dict]:
    registry_path = target_root / REGISTRY_RELATIVE_PATH
    if not registry_path.exists():
        return registry_path, default_registry()
    data = json.loads(registry_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("practice registry must be a JSON object")
    entries = data.get("entries", [])
    if not isinstance(entries, list):
        raise ValueError("practice registry entries must be a list")
    data.setdefault("version", "2026.03")
    data["entries"] = entries
    return registry_path, data


def write_registry(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def local_skill_relative_path(slug: str) -> Path:
    return LOCAL_SKILLS_ROOT / slug


def local_skill_root(target_root: Path, slug: str) -> Path:
    return target_root / local_skill_relative_path(slug)


def snippet_relative_path(slug: str) -> Path:
    return SNIPPET_ROOT / f"{slug}.md"


def snippet_path(target_root: Path, slug: str) -> Path:
    return target_root / snippet_relative_path(slug)


def read_template(relative_path: str) -> str:
    return (SKILL_ROOT / relative_path).read_text(encoding="utf-8")


def render_template(relative_path: str, replacements: dict[str, str]) -> str:
    text = read_template(relative_path)
    for key, value in replacements.items():
        text = text.replace(f"{{{{{key}}}}}", value)
    return text


def bullet_list(values: list[str], empty_fallback: str) -> str:
    if not values:
        return f"- {empty_fallback}"
    return "\n".join(f"- {value}" for value in values)


def write_files(root: Path, files: dict[Path, str]) -> None:
    for relative_path, content in files.items():
        path = root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def find_existing_entry(registry: dict, slug: str, trigger_keywords: list[str]) -> dict | None:
    wanted = {slug.lower()}
    wanted.update(keyword.lower() for keyword in trigger_keywords)
    for entry in registry.get("entries", []):
        existing = {str(entry.get("slug", "")).lower()}
        existing.update(keyword.lower() for keyword in entry.get("trigger_keywords", []))
        if wanted & existing:
            return entry
    return None


def build_entry(
    slug: str,
    summary: str,
    trigger_keywords: list[str],
    verification_commands: list[str],
    source_urls: list[str],
) -> dict:
    return {
        "slug": slug,
        "summary": summary,
        "trigger_keywords": trigger_keywords,
        "verification_commands": verification_commands,
        "source_urls": source_urls,
        "skill_path": local_skill_relative_path(slug).as_posix(),
        "status": "draft",
    }


def upsert_entry(registry: dict, entry: dict) -> None:
    for index, current in enumerate(registry.get("entries", [])):
        if current.get("slug") == entry["slug"]:
            registry["entries"][index] = entry
            return
    registry.setdefault("entries", []).append(entry)


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    values: dict[str, str] = {}
    for line in parts[1].splitlines():
        stripped = line.strip()
        if stripped and ":" in stripped:
            key, value = stripped.split(":", 1)
            values[key.strip()] = value.strip().strip('"')
    return values


def required_skill_files() -> list[Path]:
    return [
        Path("SKILL.md"),
        Path("agents") / "openai.yaml",
        Path("references") / "observations.md",
        Path("references") / "sources.md",
    ]


def validate_entry_shape(entry: dict) -> list[str]:
    errors: list[str] = []
    for field in REQUIRED_FIELDS:
        if field not in entry:
            errors.append(f"missing registry field: {field}")
    slug = str(entry.get("slug", ""))
    if slug and not validate_slug(slug):
        errors.append(f"invalid slug: {slug}")
    if not entry.get("source_urls"):
        errors.append(f"{slug or '<unknown>'}: source_urls must not be empty")
    if entry.get("status") not in STATUS_VALUES:
        errors.append(f"{slug or '<unknown>'}: invalid status")
    if entry.get("skill_path") != local_skill_relative_path(slug).as_posix():
        errors.append(f"{slug or '<unknown>'}: skill_path mismatch")
    return errors


def validate_local_skill(target_root: Path, entry: dict) -> list[str]:
    errors = validate_entry_shape(entry)
    slug = str(entry.get("slug", "<unknown>"))
    skill_root = target_root / str(entry.get("skill_path", ""))
    if not skill_root.exists():
        errors.append(f"{slug}: missing skill root")
        return errors

    for relative_path in required_skill_files():
        path = skill_root / relative_path
        if not path.exists():
            errors.append(f"{slug}: missing {relative_path.as_posix()}")

    skill_md_path = skill_root / "SKILL.md"
    if skill_md_path.exists():
        frontmatter = parse_frontmatter(skill_md_path.read_text(encoding="utf-8"))
        if frontmatter.get("name") != slug:
            errors.append(f"{slug}: SKILL.md name mismatch")
        if "description" not in frontmatter:
            errors.append(f"{slug}: SKILL.md description missing")

    openai_path = skill_root / "agents" / "openai.yaml"
    if openai_path.exists():
        if "allow_implicit_invocation: false" not in openai_path.read_text(encoding="utf-8"):
            errors.append(f"{slug}: openai.yaml must set allow_implicit_invocation: false")

    sources_path = skill_root / "references" / "sources.md"
    if sources_path.exists():
        text = sources_path.read_text(encoding="utf-8")
        for source_url in entry.get("source_urls", []):
            if source_url not in text:
                errors.append(f"{slug}: missing source url {source_url}")

    if entry.get("status") == "approved" and not snippet_path(target_root, slug).exists():
        errors.append(f"{slug}: missing promoted snippet")

    return errors


def validate_registry(target_root: Path, slug: str | None = None) -> list[str]:
    try:
        registry_path, registry = load_registry(target_root)
    except ValueError as exc:
        return [str(exc)]

    errors: list[str] = []
    if registry_path.exists() and not registry.get("entries"):
        errors.append("practice registry is empty")
        return errors

    entries = registry.get("entries", [])
    if slug is not None:
        entries = [entry for entry in entries if entry.get("slug") == slug]
        if not entries:
            return [f"missing registry entry: {slug}"]

    seen: set[str] = set()
    for entry in entries:
        current_slug = str(entry.get("slug", ""))
        if current_slug in seen:
            errors.append(f"duplicate registry slug: {current_slug}")
            continue
        seen.add(current_slug)
        errors.extend(validate_local_skill(target_root, entry))
    return errors
