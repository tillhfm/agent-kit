import json
import os
import subprocess
import sys
import unittest

PLUGIN = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "plugin")
HOOK = os.path.join(PLUGIN, "hooks", "rules.py")
sys.path.insert(0, os.path.dirname(HOOK))
import rules  # noqa: E402


def run(*args):
    out = subprocess.run([sys.executable, HOOK, *args], capture_output=True, text=True, check=True).stdout
    return json.loads(out)["hookSpecificOutput"]["additionalContext"] if out else None


def hook_parts():
    with open(os.path.join(PLUGIN, "hooks", "hooks.json")) as f:
        commands = [h["command"] for h in json.load(f)["hooks"]["SessionStart"][0]["hooks"]]
    return [c.rsplit(" ", 1)[1] for c in commands]


class RulesHookTest(unittest.TestCase):
    def test_without_a_part_the_rules_come_whole(self):
        whole = run("SessionStart")
        self.assertTrue(whole.startswith("# Agent rules"))
        self.assertNotIn("{kit}", whole)
        self.assertIn("## Commits", whole)

    def test_the_hooks_parts_hold_every_section_under_the_limit(self):
        whole = run("SessionStart")
        got = [run("SessionStart", n) for n in hook_parts()]
        self.assertIsNone(got[-1], "the last hook must stay empty, so the rules have room to grow")
        got = [g for g in got if g]
        for part in got:
            self.assertLessEqual(len(part), rules.LIMIT + 40)
        joined = got[0] + "".join(p.split("\n\n", 1)[1] for p in got[1:])
        self.assertEqual(joined, whole)

    def test_parts_split_only_at_sections(self):
        text = "# Rules\n\nintro\n" + "".join(f"## S{i}\n\n{'x' * 3000}\n" for i in range(5))
        got = rules.parts(text)
        self.assertEqual(len(got), 3)
        self.assertTrue(got[1].startswith("# Agent rules, part 2 of 3\n\n## S"))
        self.assertTrue(all(len(p) <= rules.LIMIT + 40 for p in got))

    def test_short_rules_stay_one_part(self):
        self.assertEqual(rules.parts("# Rules\n\n## A\n\nshort\n"), ["# Rules\n\n## A\n\nshort\n"])


if __name__ == "__main__":
    unittest.main()
