import os
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRACKER_FILES = [
    "plugin/rules.md",
    "plugin/skills/ship/SKILL.md",
    "plugin/skills/ship-for-review/SKILL.md",
    "plugin/skills/plan-work/SKILL.md",
    "plugin/skills/work-loop/SKILL.md",
    "plugin/skills/change-review/SKILL.md",
]


class AtelierTrackerTest(unittest.TestCase):
    def read(self, path):
        with open(os.path.join(ROOT, path)) as f:
            return f.read()

    def test_every_tracker_aware_skill_uses_atelier_json(self):
        for path in TRACKER_FILES:
            with self.subTest(path=path):
                self.assertIn("atelier --json", self.read(path))

    def test_ship_defers_orchestration_to_atelier(self):
        ship = self.read("plugin/skills/ship/SKILL.md")
        self.assertIn("`atelier/<task>`", ship)
        self.assertIn("Atelier dispatches the reviewer", ship)
        self.assertIn("Never merge under `atelier`", ship)
        self.assertIn("--kind ruling", ship)

    def test_agent_planning_leaves_area_resume_to_the_owner(self):
        plan = self.read("plugin/skills/plan-work/SKILL.md")
        self.assertNotIn("Run `atelier --json area resume", plan)

    def test_rules_stay_under_the_antigravity_limit(self):
        self.assertLess(os.path.getsize(os.path.join(ROOT, "plugin/rules.md")), 24000)


if __name__ == "__main__":
    unittest.main()
