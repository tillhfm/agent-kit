import json
import os
import subprocess
import tempfile
import unittest

HOOK = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "plugin", "hooks", "rules.py")


def run(project, event="SessionStart"):
    env = {**os.environ, "CLAUDE_PROJECT_DIR": project}
    out = subprocess.run(["python3", HOOK, event], capture_output=True, text=True, env=env, check=True).stdout
    return json.loads(out)["hookSpecificOutput"]


def hooks_path(project):
    result = subprocess.run(["git", "-C", project, "config", "--local", "core.hooksPath"], capture_output=True, text=True)
    return result.stdout.strip()


def repo(with_hooks=True):
    folder = tempfile.mkdtemp()
    subprocess.run(["git", "init", "-q", folder], check=True)
    if with_hooks:
        os.mkdir(os.path.join(folder, ".githooks"))
    return folder


class RulesTest(unittest.TestCase):
    def test_theRulesReachTheContext(self):
        output = run(repo())
        self.assertEqual(output["hookEventName"], "SessionStart")
        self.assertIn("A commit message is one line", output["additionalContext"])

    def test_aCloneUsesTheProjectHooks(self):
        project = repo()
        run(project)
        self.assertEqual(hooks_path(project), ".githooks")

    def test_aSetPathStays(self):
        project = repo()
        subprocess.run(["git", "-C", project, "config", "core.hooksPath", "elsewhere"], check=True)
        run(project)
        self.assertEqual(hooks_path(project), "elsewhere")

    def test_aProjectWithoutHooksIsLeftAlone(self):
        project = repo(with_hooks=False)
        run(project)
        self.assertEqual(hooks_path(project), "")

    def test_aSubagentChangesNothing(self):
        project = repo()
        run(project, "SubagentStart")
        self.assertEqual(hooks_path(project), "")

    def test_aFolderOutsideGitStillGetsTheRules(self):
        folder = tempfile.mkdtemp()
        os.mkdir(os.path.join(folder, ".githooks"))
        self.assertIn("commit", run(folder)["additionalContext"])


if __name__ == "__main__":
    unittest.main()
