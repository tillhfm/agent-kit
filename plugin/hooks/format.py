"""Formats and lints the file an Edit or Write changed, with the commands of the nearest .agent-kit.json.

It writes into the agent's context only when the formatter changed the file, a command failed or the linter
reported a finding. Otherwise it writes nothing.
"""

import fnmatch
import glob
import hashlib
import json
import os
import shlex
import subprocess
import sys

CONFIG = ".agent-kit.json"
MAX_LINES = 30


def find_config(path):
    folder = os.path.dirname(path)
    while True:
        candidate = os.path.join(folder, CONFIG)
        if os.path.isfile(candidate):
            return folder, candidate
        parent = os.path.dirname(folder)
        if parent == folder:
            return None, None
        folder = parent


def matches(pattern, relative):
    return fnmatch.fnmatch(relative if "/" in pattern else os.path.basename(relative), pattern)


def digest(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def run(command, path, root, env):
    kit = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    command = command.replace("{file}", shlex.quote(path)).replace("{kit}", shlex.quote(kit))
    done = subprocess.run(command, shell=True, cwd=root, env=env, capture_output=True, text=True)
    output = (done.stdout + done.stderr).strip().splitlines()
    return done.returncode, "\n".join(output[:MAX_LINES])


def main():
    tool_input = json.load(sys.stdin).get("tool_input", {})
    # Claude tools send file_path, Kimi Code tools send path.
    path = tool_input.get("file_path") or tool_input.get("path")
    if not path or not os.path.isfile(path):
        return
    root, config_path = find_config(path)
    if not root:
        return
    with open(config_path) as f:
        config = json.load(f)
    relative = os.path.relpath(path, root)
    entry = next((e for e in config.get("files", []) if any(matches(p, relative) for p in e["match"])), None)
    if not entry:
        return

    extra = [d for p in config.get("path", []) for d in sorted(glob.glob(os.path.join(root, p)))]
    env = dict(os.environ, PATH=os.pathsep.join(extra + [os.environ.get("PATH", "")]))
    notices = []
    if "format" in entry:
        before = digest(path)
        code, output = run(entry["format"], path, root, env)
        if code != 0:
            notices.append(f"agent-kit: the formatter failed on {relative}:\n{output}")
        elif digest(path) != before:
            notices.append(f"agent-kit: the formatter changed {relative}; read it again before the next edit.")
    if "lint" in entry:
        code, output = run(entry["lint"], path, root, env)
        if code != 0:
            notices.append(f"agent-kit: the linter reports on {relative}:\n{output}")
    if notices:
        context = "\n".join(notices)
        json.dump({"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": context}}, sys.stdout)


main()
