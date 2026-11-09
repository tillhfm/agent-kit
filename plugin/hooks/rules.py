"""Puts rules.md into the context of a session or a subagent. The event name is the first argument.

{kit} in the rules becomes the plugin's folder, so a rule can name the kit's scripts by path.

At the start of a session the project's own git hooks in .githooks are switched on where git does not use them yet. A
clone, such as one in a cloud session, never carries core.hooksPath, so the commit-msg hook would not run there.
"""

import json
import os
import subprocess
import sys


def use_project_hooks(project):
    """Sets core.hooksPath to .githooks in the project's repository when that folder exists and no path is set."""
    if not os.path.isdir(os.path.join(project, ".githooks")):
        return
    try:
        current = subprocess.run(
            ["git", "-C", project, "config", "--local", "core.hooksPath"], capture_output=True, text=True, timeout=5
        )
        if current.returncode == 0 and current.stdout.strip():
            return
        subprocess.run(
            ["git", "-C", project, "config", "--local", "core.hooksPath", ".githooks"], capture_output=True, timeout=5
        )
    except (OSError, subprocess.SubprocessError):
        pass


if __name__ == "__main__":
    event = sys.argv[1]
    if event == "SessionStart":
        use_project_hooks(os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd()))
    kit = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(os.path.join(kit, "rules.md")) as f:
        rules = f.read().replace("{kit}", kit)
    json.dump({"hookSpecificOutput": {"hookEventName": event, "additionalContext": rules}}, sys.stdout)
