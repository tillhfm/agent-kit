# Log lines

A log line is read by an operator who searches for it, filters it and counts it. It is an event, not a
sentence, after the events of OpenTelemetry.

## Format

`<event>: name=value name=value`

- **The event** is lowercase, without a full stop: the thing first, then what happened to it, as a
  past participle or an adjective: `settled requests removed`, `docker socket not answering`,
  `settings unreadable`. The event text is fixed, so a search for it finds every occurrence. No
  value is spliced into the event.
- **The fields** follow the colon as `name=value` pairs, separated by one space. A name is lowercase
  and names what the value is: `count`, `table`, `image`, `container`, `cause`. One name means one
  thing in every log line of the project. A value with a space is quoted: `name="Spring Market"`.
- **The cause** of a failure is the field `cause`, last: `database schema not applied: cause={cause}`.
- **Two facts of one event** share the event, joined by a comma, when both happened:
  `pull failed, local image used: image={image} local={local}`.
- **An event without values** ends without a colon: `docker socket not answering`.

Where the logging library takes structured arguments, the fields go there instead of into the
message, and the message is the event alone.

## What stays out

- **No consequence that did not happen yet**: `so nothing that logs in will start` goes. What the
  code did in response did happen and is part of the event (`database not touched`).
- **No sentence, no "we", no "please", no exclamation mark.**
- **No stack trace in the message.** The logger attaches the exception.
- **No secret and no personal data in a field**: no token, password or address. An identifier
  that names the record is enough.

## Level

- **error**: the action failed, and a human has to act.
- **warn**: the action went on in a degraded way, or a human may have to act.
- **info**: a state changed in the normal course.
- **debug**: detail for finding a fault, off in production.

## Script output

A script's progress line, read in a terminal, follows the same format: `backup written:
file={file} size={size}`. Its last line on failure, the one a person acts on, is a refusal or
failure as `patterns.md` describes, in a full sentence with the next step: `Backup failed: the
disk is full. Free space on /var and run it again.`

## Pairs

- Fails: `The database schema could not be applied, so nothing that logs in will start.`
- Passes: `database schema not applied: cause={cause}`
- Fails: `No docker socket answers, so every container route answers that the daemon is not answering.`
- Passes: `docker socket not answering`
- Fails: `Refusing to touch the database on settings that cannot be read: {cause}`
- Passes: `settings unreadable, database not touched: cause={cause}`
- Fails: `Removed {count} settled requests from {table} older than {before}.`
- Passes: `settled requests removed: count={count} table={table} before={before}`
- Fails: `could not read the log of {container}`
- Passes: `container log unreadable: container={container}`
