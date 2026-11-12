# Rules

Twelve rules, each under one of the four principles of ISO 24495-1:2023 plain language. Every rule
names its source. A text passes when every rule passes. Each pair shows a text that fails and its
rewrite that passes.

## Relevant: the reader gets what the moment needs

**R1 Only the trigger.** No sentence explains the system, a rule or the text itself. The text says
what happened or what a control does, and stops. A reader who asked for the explanation, as with a
help command or a help page, gets it. Source: ISO 24495-1, relevant.

- Fails: `You are next. The server lets players in one at a time.`
- Passes: `You are next.`
- Fails: `The payment link is being created. This message updates as soon as it is ready.`
- Passes: `Creating the payment link …`

**R2 One fact once.** What the first sentence already says, or what the screen already shows, goes.
Source: Microsoft Writing Style Guide.

- Fails: `The limit is set to {limit}. The change is saved.`
- Passes: `The limit is now {limit}.`
- Fails: `The connection was lost. You are in the waiting room. You return when the server answers.`
  The reader sees the waiting room.
- Passes: `The connection was lost. You return when the server answers.`

## Findable: the reader finds the point first

**R3 The result first.** The text opens with what happened or what is true now. A cause, a time or a
place follows it. Source: GOV.UK content design.

- Fails: `Entries changed while you were editing, so nothing of your edit was saved.`
- Passes: `Not saved: the list changed while you were editing.`

**R11 A log line is an event, then named fields.** A lowercase event, a colon, then `name=value`
pairs. No sentence, no clause that states a consequence, no full stop. Source: OpenTelemetry events.
`logs.md` holds the details.

- Fails: `Removed {count} settled requests from {table} older than {before}.`
- Passes: `settled requests removed: count={count} table={table} before={before}`

**R12 A success names what is true now.** It names the new state or the done action, never
"successfully". Source: Fluent 2 design system.

- Fails: `Your account was successfully unlinked.`
- Passes: `Your account is no longer linked.`

## Understandable: the reader understands it on the first read

**R4 Specific.** A cause or a value replaces a stock phrase such as "something went wrong", "try
again later" or "an error occurred". Source: Nielsen Norman Group error-message guidelines, Shopify
Polaris. A wait the reader can act on, such as "in a few minutes" or "after {until}", passes where
the code knows no more exact value.

- Fails: `The match cannot start right now. Try again later.`
- Passes: `No match possible: {reason}.`

**R6 Short and active.** Short sentences, verbs over nouns, active voice where the actor matters.
No "please", no exclamation mark, no filler ("currently", "simply", "just", "in order to").
Source: Hohenheim comprehensibility index (HIX), Microsoft Writing Style Guide.

- Fails: `The server is full. {online} of {max} players online. Please try again in a few minutes!`
- Passes: `The server is full: {online} of {max} players online. Try again in a few minutes.`

**R8 One term per thing.** Every thing has one term, taken from the project's term list, in every
text and every language. Where the platform has its own localised word, the project uses it.
Source: terminology management.

- Fails: `Your account is linked.` next to `Your profile is not connected.` for the same thing.
- Passes: `Your account is linked.` and `Your account is not linked.`

**R9 Typography of the language.** German follows DIN 5008, as `german.md` describes: a space before
a unit and %, „…“ as quotes, × for a count. English uses “…”, a space before a unit and none before
%. A placeholder sits where the value reads correctly. Source: DIN 5008, the language's style guide.

- Fails: `{distance}m left` and `{amount}x {item}`
- Passes: `{distance} m left` and `{amount} × {item}`

**R10 Neutral wording.** A text names people without a gender wherever a neutral word reads
naturally, such as "team member" or "everyone who helped". It uses no gender star, colon or capital
I. Source: gender-fair language guidance, limited to wording without special characters.

- Fails: `Dein Teampartner ist nicht beigetreten.`
- Passes: `Dein Teammitglied ist nicht beigetreten.`

## Usable: the reader can act on it

**R5 The next step only where the screen does not show it.** A text names what the reader does next
only when no control, prompt or obvious path shows it, or when the step is somewhere else entirely.
It never adds the system's reason for the step. Source: Nielsen Norman Group, without its advice to
explain how the system works.

- Fails: `No votes left today. Come back tomorrow.` "Today" already says when.
- Passes: `No votes left today.`
- Passes and keeps its step: `The code is wrong or expired. Sign in again for a new one.` Nothing
  else shows how to get a new code.

**R7 A control is a verb and its object.** A button or menu entry starts with the verb of what it
does and names what it acts on. A clear control needs no tooltip that explains it. Source: Apple
Human Interface Guidelines, Shopify Polaris.

- Fails: a button `OK` under a delete prompt, and a tooltip `Click to hand in items.`
- Passes: a button `Delete backup`, and a control labelled `Hand in items` without a tooltip.
