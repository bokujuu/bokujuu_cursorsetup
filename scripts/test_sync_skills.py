# -*- coding: utf-8 -*-
"""Regression checks for retirement, preservation, and cross-agent distribution."""
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from sync_skills import MARKER, sync


class SyncTests(unittest.TestCase):
    def test_retirement_and_cross_agent_sync(self):
        with tempfile.TemporaryDirectory() as work:
            home = Path(work) / 'home'
            source = Path(work) / 'source'
            (source / 'active').mkdir(parents=True)
            (source / 'active/SKILL.md').write_text('new', encoding='utf-8')
            for product in ['.codex', '.cursor', '.agents']:
                dest = home / product / 'skills'
                for name in ['active', 'fable-style-reasoning', 'user-owned']:
                    (dest / name).mkdir(parents=True)
                    (dest / name / 'SKILL.md').write_text('old', encoding='utf-8')
                (dest / MARKER).write_text('active\nfable-style-reasoning\n', encoding='utf-8-sig')
            sync(home, source=source, dry_run=True)
            self.assertFalse((home / '.codex/skill-archives').exists())
            sync(home, source=source)
            for product in ['.codex', '.cursor', '.agents']:
                dest = home / product / 'skills'
                self.assertEqual((dest / 'active/SKILL.md').read_text(), 'new')
                self.assertTrue((dest / 'user-owned/SKILL.md').exists())
                self.assertFalse((dest / 'fable-style-reasoning').exists())
            saved = list((home / '.codex/skill-archives').glob('*/.codex/fable-style-reasoning/SKILL.md'))
            self.assertEqual(len(saved), 1)
            self.assertEqual(saved[0].read_text(), 'old')
            sync(home, source=source)
            self.assertTrue(saved[0].exists())

    def test_invalid_marker_is_rejected(self):
        with tempfile.TemporaryDirectory() as work:
            home = Path(work) / 'home'
            source = Path(work) / 'source'
            source.mkdir()
            dest = home / '.codex/skills'
            dest.mkdir(parents=True)
            (dest / MARKER).write_text('../outside\n', encoding='utf-8')
            with self.assertRaises(ValueError):
                sync(home, source=source)

    def test_failed_replace_restores_old_content(self):
        with tempfile.TemporaryDirectory() as work:
            home = Path(work) / 'home'
            source = Path(work) / 'source'
            (source / 'active').mkdir(parents=True)
            (source / 'active/SKILL.md').write_text('new')
            target = home / '.codex/skills/active'
            target.mkdir(parents=True)
            (target / 'SKILL.md').write_text('old')
            with patch('sync_skills.rename_with_retry', side_effect=PermissionError):
                with self.assertRaises(PermissionError):
                    sync(home, source=source)
            self.assertEqual((target / 'SKILL.md').read_text(), 'old')
            self.assertEqual(list(target.parent.glob('.staging-*')), [])

    def test_empty_auxiliary_marker_and_claude_untouched(self):
        with tempfile.TemporaryDirectory() as work:
            home = Path(work) / 'home'
            source = Path(work) / 'source'
            source.mkdir()
            (home / '.agents/skills').mkdir(parents=True)
            claude = home / '.claude/skills/fable-style-reasoning'
            claude.mkdir(parents=True)
            (claude / 'SKILL.md').write_text('untouched')
            sync(home, source=source)
            sync(home, source=source)
            self.assertEqual((claude / 'SKILL.md').read_text(), 'untouched')


if __name__ == '__main__':
    unittest.main()
