from __future__ import annotations

import argparse
from pathlib import Path

import practice_helpers as helpers


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate repo-local draft or approved skills created by implement-with-practices.")
    parser.add_argument("--target", required=True)
    parser.add_argument("--slug")
    args = parser.parse_args()

    errors = helpers.validate_registry(Path(args.target).resolve(), slug=args.slug)
    if errors:
        for error in errors:
            print(error)
        return 1

    print("validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
