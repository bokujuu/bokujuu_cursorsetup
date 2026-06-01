from __future__ import annotations

import argparse
from pathlib import Path

import practice_helpers as helpers


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Scaffold a repo-local draft skill from a successful implementation pattern.")
    parser.add_argument("--target", required=True)
    parser.add_argument("--slug", required=True)
    parser.add_argument("--summary", required=True)
    parser.add_argument("--trigger-keyword", action="append", default=[])
    parser.add_argument("--verification-command", action="append", default=[])
    parser.add_argument("--source-url", action="append", default=[])
    parser.add_argument("--adoption-reason", default="Document the reason this approach is preferred in this repository.")
    parser.add_argument("--avoid", action="append", default=[])
    parser.add_argument("--observation", action="append", default=[])
    parser.add_argument("--default-prompt", default="")
    parser.add_argument("--script-name", default="")
    parser.add_argument("--script-summary", default="")
    parser.add_argument("--force", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()

    if not helpers.validate_slug(args.slug):
        print(f"invalid slug: {args.slug}")
        return 1

    trigger_keywords = helpers.normalize_lines(args.trigger_keyword)
    verification_commands = helpers.normalize_lines(args.verification_command)
    source_urls = helpers.normalize_lines(args.source_url)
    avoids = helpers.normalize_lines(args.avoid)
    observations = helpers.normalize_lines(args.observation)

    if not trigger_keywords:
        print("missing trigger keywords")
        return 1
    if not verification_commands:
        print("missing verification commands")
        return 1
    if not source_urls:
        print("missing source urls")
        return 1

    target_root = Path(args.target).resolve()
    registry_path, registry = helpers.load_registry(target_root)
    existing = helpers.find_existing_entry(registry, args.slug, trigger_keywords)
    if existing is not None and existing.get("slug") != args.slug:
        if args.force:
            print(f"conflicting existing practice: {existing['slug']}")
            return 1
        print(f"skipped-existing-practice: {existing['slug']}")
        return 0
    if existing is not None and not args.force:
        print(f"skipped-existing-practice: {existing['slug']}")
        return 0

    title = helpers.title_from_slug(args.slug)
    skill_root = helpers.local_skill_root(target_root, args.slug)
    if skill_root.exists() and not args.force:
        print(f"skill already exists: {skill_root}")
        return 1

    description = (
        f"Repo-local implementation practice for {', '.join(trigger_keywords)}. "
        f"Use when working in this repository on {args.summary}."
    )
    default_prompt = args.default_prompt or (
        f"Use the local skill at .codex/skills/{args.slug} to follow the repository practice for {args.summary}."
    )

    replacements = {
        "SLUG": args.slug,
        "TITLE": title,
        "SUMMARY": args.summary,
        "DESCRIPTION": description,
        "SHORT_DESCRIPTION": f"Follow the repo-local practice for {args.summary}.",
        "DEFAULT_PROMPT": default_prompt,
        "TRIGGER_BULLETS": helpers.bullet_list([f"`{value}`" for value in trigger_keywords], "No trigger keywords recorded."),
        "VERIFICATION_BULLETS": helpers.bullet_list([f"`{value}`" for value in verification_commands], "No verification commands recorded."),
        "ADOPTION_REASON": args.adoption_reason,
        "AVOID_BULLETS": helpers.bullet_list(avoids, "No explicit pitfalls recorded yet."),
        "OBSERVATION_BULLETS": helpers.bullet_list(observations, "No additional experiment notes recorded yet."),
        "SOURCE_BULLETS": helpers.bullet_list(source_urls, "No source URLs recorded."),
        "SKILL_PATH": helpers.local_skill_relative_path(args.slug).as_posix(),
        "SCRIPT_SUMMARY": args.script_summary or "this local practice",
    }

    files: dict[Path, str] = {
        Path("SKILL.md"): helpers.render_template("assets/templates/local-skill/SKILL.md.template", replacements),
        Path("agents") / "openai.yaml": helpers.render_template(
            "assets/templates/local-skill/agents.openai.yaml.template",
            replacements,
        ),
        Path("references") / "observations.md": helpers.render_template(
            "assets/templates/local-skill/references.observations.md.template",
            replacements,
        ),
        Path("references") / "sources.md": helpers.render_template(
            "assets/templates/local-skill/references.sources.md.template",
            replacements,
        ),
    }
    if args.script_name:
        files[Path("scripts") / f"{args.script_name}.py"] = helpers.render_template(
            "assets/templates/local-skill/scripts.helper.py.template",
            replacements,
        )

    helpers.write_files(skill_root, files)

    entry = helpers.build_entry(
        slug=args.slug,
        summary=args.summary,
        trigger_keywords=trigger_keywords,
        verification_commands=verification_commands,
        source_urls=source_urls,
    )
    helpers.upsert_entry(registry, entry)
    helpers.write_registry(registry_path, registry)

    print(f"created: {skill_root}")
    print(f"registry: {registry_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
