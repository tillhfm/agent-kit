"""Puts rules.md into the context of a session or a subagent. The event name is the first argument.

{kit} in the rules becomes the plugin's folder, so a rule can name the kit's scripts by path.

Claude Code shows a hook's context only as a short preview once it passes about 10,000 characters,
so its hooks ask for the rules in parts, the part number as the second argument. A part holds whole
sections, says which part of how many it is and stays under LIMIT; a part number out of range
prints nothing. Without a part number the rules come whole, for a host without that limit.
"""

import json
import os
import sys

LIMIT = 9000


def parts(rules):
    sections, current = [], []
    for line in rules.splitlines(keepends=True):
        if line.startswith("## ") and current:
            sections.append("".join(current))
            current = []
        current.append(line)
    sections.append("".join(current))
    chunks = [""]
    for section in sections:
        if chunks[-1] and len(chunks[-1]) + len(section) > LIMIT:
            chunks.append("")
        chunks[-1] += section
    if len(chunks) == 1:
        return chunks
    count = len(chunks)
    return [f"# Agent rules, part {i} of {count}\n\n{c}" for i, c in enumerate(chunks, 1)]


def main():
    event = sys.argv[1]
    kit = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(os.path.join(kit, "rules.md")) as f:
        rules = f.read().replace("{kit}", kit)
    if len(sys.argv) > 2:
        chunks = parts(rules)
        number = int(sys.argv[2])
        if not 1 <= number <= len(chunks):
            return
        rules = chunks[number - 1]
    json.dump({"hookSpecificOutput": {"hookEventName": event, "additionalContext": rules}}, sys.stdout)


if __name__ == "__main__":
    main()
