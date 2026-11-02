import json
import os
import subprocess
import sys
import tempfile
import unittest

HOOK = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "plugin", "hooks", "format.py")
UPPER = f"{sys.executable} -c \"import sys; p=sys.argv[1]; s=open(p).read(); open(p,'w').write(s.upper())\" {{file}}"
FAIL = "echo 'line 1: unused variable' && exit 1"


def read(path):
    with open(path) as f:
        return f.read()


def run_hook(path):
    event = {"hook_event_name": "PostToolUse", "tool_name": "Edit", "tool_input": {"file_path": path}}
    done = subprocess.run([sys.executable, HOOK], input=json.dumps(event), capture_output=True, text=True, check=True)
    return json.loads(done.stdout)["hookSpecificOutput"]["additionalContext"] if done.stdout else None


class FormatHookTest(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()

    def project(self, config):
        with open(os.path.join(self.root, ".agent-kit.json"), "w") as f:
            json.dump(config, f)

    def file(self, name, text):
        path = os.path.join(self.root, name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(text)
        return path

    def test_aFileOutsideAnyProjectGetsNoNotice(self):
        self.assertIsNone(run_hook(self.file("a.ts", "x")))

    def test_aReformattedFileGetsOneLine(self):
        self.project({"files": [{"match": ["*.ts"], "format": UPPER}]})
        path = self.file("src/a.ts", "x")
        notice = run_hook(path)
        self.assertEqual(read(path), "X")
        self.assertIn("src/a.ts", notice)
        self.assertEqual(len(notice.splitlines()), 1)

    def test_anUnchangedFileGetsNoNotice(self):
        self.project({"files": [{"match": ["*.ts"], "format": UPPER}]})
        self.assertIsNone(run_hook(self.file("a.ts", "X")))

    def test_aFileNoEntryMatchesGetsNoNotice(self):
        self.project({"files": [{"match": ["*.java"], "format": UPPER}]})
        path = self.file("a.ts", "x")
        self.assertIsNone(run_hook(path))
        self.assertEqual(read(path), "x")

    def test_aPatternWithASlashMatchesThePathInTheProject(self):
        self.project({"files": [{"match": ["web/*.ts"], "format": UPPER}]})
        self.assertIsNone(run_hook(self.file("other/a.ts", "x")))
        self.assertIsNotNone(run_hook(self.file("web/a.ts", "x")))

    def test_aLintFindingReachesTheAgent(self):
        self.project({"files": [{"match": ["*.ts"], "lint": FAIL}]})
        self.assertIn("unused variable", run_hook(self.file("a.ts", "X")))

    def test_aCleanLintGetsNoNotice(self):
        self.project({"files": [{"match": ["*.ts"], "lint": "echo 'Found 0 warnings'"}]})
        self.assertIsNone(run_hook(self.file("a.ts", "X")))

    def test_aFailingFormatterReachesTheAgent(self):
        self.project({"files": [{"match": ["*.ts"], "format": "echo 'syntax error at 3:1' >&2 && exit 2"}]})
        self.assertIn("syntax error at 3:1", run_hook(self.file("a.ts", "X")))

    def test_thePathEntriesComeFirstOnThePath(self):
        os.makedirs(os.path.join(self.root, "tools", "v1", "bin"))
        tool = self.file("tools/v1/bin/shout", f"#!/bin/sh\nexec {UPPER.replace('{file}', '\"$1\"')}\n")
        os.chmod(tool, 0o755)
        self.project({"path": ["tools/*/bin"], "files": [{"match": ["*.ts"], "format": "shout {file}"}]})
        path = self.file("a.ts", "x")
        self.assertIsNotNone(run_hook(path))
        self.assertEqual(read(path), "X")

    def test_theNearestConfigWins(self):
        self.project({"files": [{"match": ["*.ts"], "lint": FAIL}]})
        self.file("inner/.agent-kit.json", '{"files": []}')
        self.assertIsNone(run_hook(self.file("inner/a.ts", "x")))


if __name__ == "__main__":
    unittest.main()
