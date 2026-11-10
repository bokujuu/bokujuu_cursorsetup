# -*- coding: utf-8 -*-
"""Copy behavior for the imozuru upstream refresh. Network is not used."""
from datetime import datetime, timedelta, timezone
from pathlib import Path
import tempfile
import unittest

from update_imozuru import refresh


JST = timezone(timedelta(hours=9))
SHA = "abc123def4567890abc123def4567890abc123de"


def write_upstream(root: Path) -> None:
    skill = root / "skills" / "imozuru"
    (skill / "scripts").mkdir(parents=True)
    (skill / "references").mkdir(parents=True)
    (skill / "SKILL.md").write_text("---\nname: imozuru\n---\nbody\n", encoding="utf-8")
    (skill / "scripts" / "fetch.py").write_text("print('fetch')\n", encoding="utf-8")
    (skill / "references" / "theory.md").write_text("theory\n", encoding="utf-8")
    (root / "tests").mkdir()
    (root / "tests" / "test_fetch.py").write_text("nope\n", encoding="utf-8")
    (root / "LICENSE").write_text("MIT License\n\nCopyright (c) 2026 MaryCache\n", encoding="utf-8")
    (root / ".claude-plugin").mkdir()
    (root / ".claude-plugin" / "plugin.json").write_text('{"version": "9.9.9"}\n', encoding="utf-8")


class UpdateImozuruTests(unittest.TestCase):
    def test_replaces_skill_and_keeps_only_local_additions(self):
        with tempfile.TemporaryDirectory() as work:
            work_path = Path(work)
            upstream = work_path / "upstream"
            repo = work_path / "repo"
            write_upstream(upstream)
            old = repo / "skills" / "imozuru" / "scripts"
            old.mkdir(parents=True)
            (repo / "skills" / "imozuru" / "SKILL.md").write_text("stale\n", encoding="utf-8")
            (old / "gone.py").write_text("gone\n", encoding="utf-8")
            when = datetime(2026, 11, 10, 23, 20, tzinfo=JST)

            status = refresh(upstream, repo, SHA, when, dry_run=False)

            dest = repo / "skills" / "imozuru"
            self.assertEqual(status, "updated")
            self.assertIn("body", (dest / "SKILL.md").read_text(encoding="utf-8"))
            self.assertFalse((dest / "scripts" / "gone.py").exists())
            self.assertTrue((dest / "scripts" / "fetch.py").is_file())
            self.assertFalse((dest / "tests").exists())
            self.assertIn("Copyright (c) 2026 MaryCache", (dest / "LICENSE").read_text(encoding="utf-8"))
            sources = (dest / "references" / "sources.md").read_text(encoding="utf-8")
            self.assertIn(SHA, sources)
            self.assertIn("9.9.9", sources)
            self.assertIn("python scripts/update_imozuru.py", sources)
            self.assertIn("2026/11/10 23:20", sources)
            self.assertIn("theory", (dest / "references" / "theory.md").read_text(encoding="utf-8"))

            again = refresh(upstream, repo, SHA, when.replace(minute=30), dry_run=False)
            self.assertEqual(again, "current")
            self.assertIn("2026/11/10 23:20", (dest / "references" / "sources.md").read_text(encoding="utf-8"))

    def test_dry_run_does_not_write(self):
        with tempfile.TemporaryDirectory() as work:
            work_path = Path(work)
            upstream = work_path / "upstream"
            repo = work_path / "repo"
            write_upstream(upstream)
            when = datetime(2026, 11, 10, 23, 20, tzinfo=JST)

            status = refresh(upstream, repo, SHA, when, dry_run=True)

            self.assertEqual(status, "would-update")
            self.assertFalse((repo / "skills" / "imozuru").exists())


if __name__ == "__main__":
    unittest.main()
