from __future__ import annotations

import argparse
from pathlib import Path

import practice_helpers as helpers


def main() -> int:
    parser = argparse.ArgumentParser(description="Promote a repo-local draft skill to approved and generate an AGENTS snippet.")
    parser.add_argument("--target", required=True)
    parser.add_argument("--slug", required=True)
    args = parser.parse_args()

    target_root = Path(args.target).resolve()
    errors = helpers.validate_registry(target_root, slug=args.slug)
    if errors:
        for error in errors:
            print(error)
        return 1

    registry_path, registry = helpers.load_registry(target_root)
    entry = next(entry for entry in registry["entries"] if entry.get("slug") == args.slug)
    entry["status"] = "approved"

    replacements = {
        "TITLE": helpers.title_from_slug(args.slug),
        "SUMMARY": entry["summary"],
        "SKILL_PATH": entry["skill_path"],
        "VERIFICATION_BULLETS": helpers.bullet_list(
            [f"`{value}`" for value in entry.get("verification_commands", [])],
            "No verification commands recorded.",
        ),
    }
    snippet_rel = helpers.snippet_relative_path(args.slug)
    helpers.write_files(
        target_root,
        {
            snippet_rel: helpers.render_template(
                "assets/templates/snippets/AGENTS.md.append.md.template",
                replacements,
            )
        },
    )
    helpers.write_registry(registry_path, registry)

    print(f"approved: {args.slug}")
    print(f"snippet: {target_root / snippet_rel}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
