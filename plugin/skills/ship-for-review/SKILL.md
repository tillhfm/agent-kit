---
name: ship-for-review
description: Take one sub-item through ship up to and including the merge, then put the evidence for the owner's look - screenshots and, for UI, a short video - into its area item for the area report. Use for items whose result no check can prove - a design, a proposal, wording without a checkable goal - and for items that say "Ends with a review."
---

# Ship for review

Follow `ship` from the start to the merge, with its proof, review and merge gate. Only the end
differs: the owner looks at the result in the area report and accepts it or asks for another
iteration.

## Evidence for the look

After the merge, record what the owner needs to judge the result without running anything:

- **Screenshots** of every changed page or state at 390, 768 and 1440 pixels width, taken from the
  merged code with Playwright. A dark and a light theme each, where the project has both.
- **A video** of the flow for an interactive change: a Playwright recording as WebM, under a
  minute, of the steps a user takes.
- **No UI**: the text, the output or the file that was made, quoted or attached.

Attach the files to the area item, where the owner reads. Name every difference between the result
and what was intended.

## Report

`finish <sub-item> --done` with the report of `ship`. Its part **For the owner** holds:

- **What to look at**: the question the owner answers, in one sentence, and the attached files.
- **What a human has to do**: anything the session could not do itself, such as a look in a
  Minecraft client or a test with a real account. Omitted when there is nothing.

The area report collects these lines. An answer that asks for changes comes back as the area item
in `ready` with the answer as a comment. The next session writes the next iteration from it.

Then it proposes the next line as the last step of `ship` says.

## Switching mid-way

A session in `ship` that finds its goal cannot be checked by itself switches to this skill and
says so in the report, as a ruling.
