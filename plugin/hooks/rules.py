"""Puts rules.md into the context of a session or a subagent. The event name is the first argument.

{kit} in the rules becomes the plugin's folder, so a rule can name the kit's scripts by path.
"""

import json
import os
import sys

event = sys.argv[1]
kit = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(kit, "rules.md")) as f:
    rules = f.read().replace("{kit}", kit)
json.dump({"hookSpecificOutput": {"hookEventName": event, "additionalContext": rules}}, sys.stdout)
