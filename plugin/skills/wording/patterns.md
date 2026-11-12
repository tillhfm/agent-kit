# Patterns

One pattern per kind of text, after the message types of the Fluent 2 and Atlassian design systems.
Each has a template, a text that fails and its rewrite that passes. `{…}` is a value the code fills
in. A part in `[…]` is written only when its condition holds.

## Success

`<thing> is now <state>.` or `<thing> <done action>.`

The new state, never "successfully" (R12). No second sentence that repeats it as "saved" or "done"
(R2).

- Fails: `The limit is set to {limit}. The change is saved.`
- Passes: `The limit is now {limit}.`

## Refusal or failure

`<what did not happen>: <cause>. [<next step>.]`

The refused or failed action first (R3), then its cause or the value that decides it (R4). The next
step only where nothing else shows it (R5). No sentence on the rule behind the refusal (R1). When
the refused action is the one the reader just took, the cause alone is the text. When nothing
changed, a failure may say so in two words.

- Fails: `That failed. Nothing was changed. The log names the reason.`
- Passes: `Failed: {cause}. Nothing changed.`
- Fails: `This file is not yours. Only the person who uploaded it, or an admin, can delete it.`
- Passes: `This file is not yours.`

## Warning

`<what will happen> <when>. [<what prevents it>.]`

The coming event and its time. What the reader can do against it, if anything. No "warning",
"note" or "attention" as a word: the place or the style marks the warning.

- Fails: `Warning! Please note that the server will restart soon, so make sure to log out.`
- Passes: `The server restarts in {minutes} minutes.`

## Countdown

`<event> in {time}` or `{time} until <event>`

A running value without a sentence. The unit follows the language's typography (R9).

- Fails: `There are {time} left before the voting will close.`
- Passes: `Voting closes in {time}`

## State

`<state>` or `<thing> <state>`

What is true, as short as the place allows: a label, a badge, a status line. A state that is the
normal case says nothing.

- Fails: `This offer will expire after {left} has passed.`
- Passes: `Expires in {left}`

## Button

`<verb> <object>`

The verb of what the control does, then what it acts on, in sentence case, without a full stop
(R7). A destructive action names its object. German uses the infinitive, as `german.md` describes.

- Fails: `OK`, `Submit`, `Click here`, `Yes`
- Passes: `Delete backup`, `Take all`, `Hand in items`

## Tooltip

`<what the control and the screen do not show>`

Only a fact the control cannot carry: a hidden condition, a key, a second way to use it. A tooltip
that repeats the label, or explains a clear control, goes (R2, R7).

- Fails: `Click to hand in items.` on a control labelled `Hand in items`
- Passes: no tooltip
- Passes and stays: `Shift-click to select a range.` The screen shows this way to use the list
  nowhere else.

## Empty state

`No <things> [yet]. [<how one appears>.]`

What is missing. How it gets filled only when no control on the same screen does it (R5).

- Fails: `There is currently nothing to display here because no backups have been created.`
- Passes: `No backups yet.` beside a `Create backup` button

## Announcement

`<event>. [<when and where>.] [<one thanks>.]`

The event first, then its time and place. One thanks at most, without an exclamation mark (R6).

- Fails: `Big news!!! {user} has just donated {amount} to the server! Thank you so much!`
- Passes: `{user} donated {amount}. Thank you.`

## Help text

`<what it does>. [<how to use it>.]`

The one kind that explains, because the reader asked for it (R1): a help command, a help page, a
form field's description. It still follows R2 to R12.

- Passes: `Sends a private message to a player on the network.`

## Log line

`<event>: name=value name=value`

A lowercase event and named fields (R11). `logs.md` holds the rules and the script output.

- Fails: `pull failed for {image}; using the local image {local}`
- Passes: `pull failed, local image used: image={image} local={local}`
