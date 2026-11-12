import json
import os
import subprocess
import tempfile
import unittest

HOOK = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "plugin", "hooks", "hooks_path.py")


def git(folder, *args):
    return subprocess.run(["git", "-C", folder, *args], capture_output=True, text=True)


def run(folder, cwd=None):
    result = subprocess.run(
        ["python3", HOOK], input=json.dumps({"cwd": cwd or folder}), capture_output=True, text=True
    )
    return result.returncode, result.stdout, git(folder, "config", "--local", "--get", "core.hooksPath").stdout.strip()


def clone(hook=True):
    folder = tempfile.mkdtemp()
    git(folder, "init", "-q")
    if hook:
        os.makedirs(os.path.join(folder, ".githooks"))
        open(os.path.join(folder, ".githooks", "commit-msg"), "w").close()
    return folder


class HooksPathTest(unittest.TestCase):
    def test_aCloneWithTheHookGetsTheHooksPath(self):
        self.assertEqual(run(clone()), (0, "", ".githooks"))

    def test_aSubfolderOfTheCloneIsEnough(self):
        folder = clone()
        os.makedirs(os.path.join(folder, "app"))
        self.assertEqual(run(folder, os.path.join(folder, "app"))[2], ".githooks")

    def test_aHooksPathOfTheClonesOwnStays(self):
        folder = clone()
        git(folder, "config", "core.hooksPath", "other")
        self.assertEqual(run(folder)[2], "other")

    def test_aCloneWithoutTheHookIsLeftAlone(self):
        self.assertEqual(run(clone(hook=False)), (0, "", ""))

    def test_aFolderOutsideGitIsLeftAlone(self):
        folder = tempfile.mkdtemp()
        result = subprocess.run(["python3", HOOK], input=json.dumps({"cwd": folder}), capture_output=True, text=True)
        self.assertEqual((result.returncode, result.stdout), (0, ""))
