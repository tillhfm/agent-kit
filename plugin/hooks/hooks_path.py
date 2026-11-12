"""Turns on the project's git hooks at the start of a session.

A project keeps its `commit-msg` hook in `.githooks/`, and `core.hooksPath` points git there. That setting
lives in the clone, not in the repository, so a fresh clone, such as the one a cloud session starts in, commits
without the hook. This sets it when the project has `.githooks/commit-msg` and the clone sets no hooks path of
its own. It prints nothing and never fails the session.
"""

import json
import os
import subprocess
import sys


def git(folder, *args):
    return subprocess.run(["git", "-C", folder, *args], capture_output=True, text=True, timeout=5)


def main():
    try:
        folder = json.load(sys.stdin).get("cwd") or os.getcwd()
    except (ValueError, AttributeError):
        folder = os.getcwd()
    top = git(folder, "rev-parse", "--show-toplevel")
    if top.returncode != 0:
        return
    root = top.stdout.strip()
    if not os.path.isfile(os.path.join(root, ".githooks", "commit-msg")):
        return
    if git(root, "config", "--local", "--get", "core.hooksPath").returncode == 0:
        return
    git(root, "config", "--local", "core.hooksPath", ".githooks")


try:
    main()
except Exception:
    pass
