# -*- coding: utf-8 -*-
"""Hooks must remain quiet unless a repository opted in."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent


class HookTests(unittest.TestCase):
    def run_hook(self, name, event, cwd):
        result = subprocess.run([sys.executable, str(ROOT / 'hooks' / name), event],
                                input=json.dumps({'cwd': str(cwd)}), capture_output=True,
                                text=True, check=True, timeout=10)
        return json.loads(result.stdout)

    def test_quiet_by_default_even_with_stale_plan(self):
        with tempfile.TemporaryDirectory() as work:
            root = Path(work)
            (root / '.cursor/plans').mkdir(parents=True)
            (root / '.cursor/plans/old.plan.md').write_text('status: pending')
            for name, event in [('handoff-stop-check.py', 'stop'),
                                ('handoff-stop-check.py', 'subagentStop'),
                                ('knowledge-capture-nudge.py', 'sessionStart')]:
                self.assertEqual(self.run_hook(name, event, root), {})
            (root / '.cursor/handoff-recovery.local.md').write_text('verify here')
            self.assertIn('followup_message', self.run_hook('handoff-stop-check.py', 'stop', root))
            (root / '.cursor/knowledge-capture.local.md').write_text('capture here')
            self.assertIn('additional_context', self.run_hook('knowledge-capture-nudge.py', 'sessionStart', root))


if __name__ == '__main__':
    unittest.main()
