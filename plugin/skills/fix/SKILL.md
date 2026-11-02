---
name: fix
description: Find and fix a bug, or build a behaviour test-first - a failing check before any change, then red, green, verified where it lives. Use when something is broken, throws, fails, is slow or behaves wrong, and for any change whose behaviour a test can pin.
---

# Fix

The whole skill is one rule: **nothing is fixed until you watched it fail and then watched it
pass.** A green test you never saw red proves nothing.

## 1. A loop that goes red

Before reading code for a theory, build one command that shows *this* symptom, fast and every time.
In order of preference: a failing test at the seam where the bug lives; a `curl` or CLI call with
a fixture; a replayed payload or log; a small harness around the one code path; the running system
itself, where the project has one the session may use.

Run it and show its output, with secrets redacted. If no loop can be built, say what you tried and
ask in the chat. Do not guess.

A timing bug is made more frequent by narrowing the window, not by loading the machine.

## 2. Shrink it

Cut inputs, steps and config one at a time while it stays red. What is left is the cause's
neighbourhood and the future regression test.

## 3. Hypotheses, then probes

Write three to five ranked, falsifiable hypotheses: "if X is the cause, changing Y makes it go
away". Test them one variable at a time. Tag temporary logging with a unique prefix
(`[DEBUG-7f3a]`) so one grep removes it.

## 4. Test, fix, verify

1. Turn the minimal case into a test at a seam where the real pattern occurs. If no such seam
   exists, that is a finding: say so in the item instead of writing a shallow test.
2. Watch it fail.
3. Fix, with the smallest change that makes it pass.
4. Watch it pass, then run the original loop again.
5. Run the project's check on what you touched.
6. Remove the tagged logging and any throwaway harness.

The observation goes into the item.

## Building something new

The same loop without a bug: one behaviour at a time, test first at a public seam, see it red,
make it green, next. No tests written ahead for behaviour that does not exist yet, no mocks of
the module's own internals, and no expected value computed the way the code computes it.
