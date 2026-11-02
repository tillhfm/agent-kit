import os
import subprocess
import tempfile
import unittest

HOOK = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "plugin", "templates", "commit-msg")


def accepts(message, tracker="", *args):
    with open(HOOK) as f:
        script = f.read().replace("tracker=''", f"tracker='{tracker}'")
    with tempfile.TemporaryDirectory() as folder:
        hook, msg = os.path.join(folder, "commit-msg"), os.path.join(folder, "MSG")
        with open(hook, "w") as f:
            f.write(script)
        with open(msg, "w") as f:
            f.write(message)
        env = {k: v for k, v in os.environ.items() if k != "CI"}
        return subprocess.run(["sh", hook, msg, *args], capture_output=True, env=env).returncode == 0


class CommitMsgTest(unittest.TestCase):
    def test_oneConventionalLinePasses(self):
        self.assertTrue(accepts("feat(steward): the card names the languages\n"))
        self.assertTrue(accepts("fix: the hook reads the catalog\n# a comment git strips\n"))

    def test_aBodyIsRefused(self):
        self.assertFalse(accepts("feat: a thing\n\nBecause of reasons.\n"))

    def test_aSubjectWithoutTypeIsRefused(self):
        self.assertFalse(accepts("add a thing\n"))

    def test_anUppercaseStartOrATrailingPeriodIsRefused(self):
        self.assertFalse(accepts("feat: The card names the languages\n"))
        self.assertFalse(accepts("feat: the card names the languages.\n"))

    def test_aModelOrItsVendorIsRefused(self):
        self.assertFalse(accepts("feat: a thing\n\nCo-Authored-By: Claude <noreply@anthropic.com>\n"))
        self.assertFalse(accepts("docs: written with opus\n"))
        self.assertFalse(accepts("docs: written with copilot\n"))

    def test_theAgentFilesOfAProjectMayBeNamed(self):
        self.assertTrue(accepts("docs: the guide in CLAUDE.md names the default branch\n"))
        self.assertTrue(accepts("- `.claude/settings.json` enables the plugin\n", "", "--names-only"))
        self.assertFalse(accepts("docs: claude writes the guide\n"))

    def test_aBotCoAuthorIsRefused(self):
        self.assertFalse(accepts("chore: bump\nCo-authored-by: dependabot[bot] <x@y>\n"))

    def test_aTrackerIdIsRefusedOnlyWhenTheProjectHasATracker(self):
        self.assertTrue(accepts("fix: the NT2-708 case\n"))
        self.assertFalse(accepts("fix: the NT2-708 case\n", tracker="NT[0-9]+-[0-9]+"))
        self.assertTrue(accepts("fix: utf-8 and UTF-8 stay\n", tracker="NT[0-9]+-[0-9]+"))

    def test_aMergeAndAFixupPassOutsideCi(self):
        self.assertTrue(accepts("Merge branch 'main'\n\nsome body\n"))
        self.assertTrue(accepts("fixup! feat: a thing\n"))

    def test_aPullRequestBodyIsCheckedForNamesOnly(self):
        body = "Two changes:\n\n- the hook reads the catalog\n- the card names the languages\n"
        self.assertTrue(accepts(body, "", "--names-only"))
        self.assertFalse(accepts(body + "Generated with a tool\n", "", "--names-only"))
        self.assertFalse(accepts(body + "See NT2-708.\n", "NT[0-9]+-[0-9]+", "--names-only"))


if __name__ == "__main__":
    unittest.main()
