---
name: wording
description: The wording standard for every text a user reads in an interface, a message or a log - rules after ISO 24495-1 plain language, a pattern per kind of text, German rules and a cold read. Use when writing, changing or reviewing such a text, from a button or an error to a log line.
---

# Wording

Every text a user reads in an interface, a message or a log says only what made it appear: what
happened, what is true now, or what a control does. It never explains the system, a rule or itself.
Agent prose (commits, pull requests, tracker items, chat) follows the Text section of the agent rules
instead.

The project decides what is its own: its term list, the languages it writes, du or Sie in German, and
any rule of its `CONVENTIONS.md` that is stricter than this skill. A project rule wins for its
project.

## Steps

For each text the change writes or touches:

1. **Name the kind of text**: success, refusal or failure, warning, countdown, state, button, tooltip,
   empty state, announcement, help text or log line. Name also what triggers it and what the reader
   sees at that moment. A text that is two kinds at once is split, or written as the kind the reader
   meets first.
2. **Apply its pattern** from `patterns.md`, and the rules R1 to R12 in `rules.md`. A log line or a
   script's output follows `logs.md`. A German text follows `german.md` too.
3. **Check every term** against the project's term list, usually in its `CONVENTIONS.md`. One thing
   has one term in every text of the project, in every language. A word the list does not have is
   taken from the platform's own localisation before a new one is coined, and added to the list.
4. **Run the cold read** below. A text whose answer misses is written again.
5. **Write each changed text as before and after**, with the rules that changed it, in the pull
   request or the tracker item. An unchanged text that was checked is listed as unchanged.

`examples.md` holds reworked texts with the rules that changed them.

## Limits

- **A place that limits a text wins over the patterns**: a status line, a button, a label, a push
  notification. The text keeps the result and drops the rest.
- **A value spliced into another text** is written to read correctly in every text that uses it:
  case, article, number and the sentence around it.
- **A text that needs a value the code does not pass**, such as a refusal's reason, a failure's cause
  or an amount paid, gets the value: the change adds it to the code. A stock phrase in its place
  fails R4.
- **A text nobody renders any more** is deleted, and the deletion is listed with the changed texts.

## Cold read

A fresh subagent reads the text as a stranger to the project. It gets only the text, with its values
filled in, and one sentence on what triggered it and where it appears ("after the user clicks
Save, below the form"). It gets no rule, no pattern, no code and no intended meaning. It answers:

- **What happened?**
- **What do I do now?** "Nothing" is a valid answer.

A log line gets one question instead: **what happened, and which value identifies it?**

The session compares each answer with the meaning the text has to carry. Where the answer misses or
adds something, the text is rewritten and read cold again, by another fresh subagent. A text that
still misses after the third reading is reported with the reason, such as a value the code cannot
give.

Many texts go to one subagent at once, as a numbered list, each with its own trigger. The subagent
answers each text on its own and is told that the texts are unrelated. A small, fast model is enough
for the reader.
