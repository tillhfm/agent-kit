# Design

How <project> looks, for people and agents. Every value lives once, as a token in `<theme stylesheet>`.
This file names the tokens and never repeats a value.

`design-tokens.test.ts` fails the build on a class with a bracketed value that names no token, and on a
spacing step off the scale. A token of Tailwind's default theme counts as a token unless the theme resets
its namespace. The test reads classes only: a declaration in a stylesheet and the rules of Surfaces are
checked in review.

## Direction

- **Personality**: <two or three words, and what follows from them for the interface>.
- **Foundation**: <light or dark, the neutral, the one accent>.
- **Depth**: <what sets a surface apart: a border, a shadow or a change of tone>.

## Spacing

One scale for padding, margin, gap and space, in steps of `--spacing`: 1px, every 2px up to 12px,
every 4px up to 24px, every 8px up to 48px, then 64, 80, 96 and 128px. `SPACING_STEPS` in
`design-tokens.test.ts` lists these steps, and the test refuses any other.

- Parts that belong together are closer to each other than to the padding around them.
- Groups that do not belong together are further apart than that padding.
- One component keeps to few steps: one for its padding, one between its parts.
- A size (width, height, an inset) is any multiple of `--spacing`. A size that recurs, or that is
  not a multiple, becomes a token.

## Surfaces

Surfaces stack in three levels, each with a background token and the foreground token that goes on
it:

| Level | What | Tokens |
| --- | --- | --- |
| page | the ground everything stands on | <`background`, `foreground`> |
| raised | a card, a panel, a table, an input | <tokens> |
| floating | a menu, a popover, a dialog, a drawer, a toast | <tokens> |

- A surface takes its level's tokens and no other level's.
- A level above sets itself apart by the depth that Direction names.
- A border is one hairline in the border token. A divider is the same line.
- A nested surface's radius is the outer radius less the space between them, never more.
- A modal surface has a backdrop. A surface that does not block the page has none.
- Every control shows focus as the same ring, in the ring token.
- A colour comes from a token. A token with an opacity (`bg-muted/50`) still counts as the token.

## Colour

<The project's colour tokens and what each is for.>

## Type

<The project's fonts and text sizes, and what each is for.>

## Components

<Each component of the interface and when it is used rather than another.>

## Content

<What draws its own look, such as a picture, a game or another application's interface. Its classes
are exempt by name in `design-tokens.test.ts`.>

## Decisions

| Decision | Why |
| --- | --- |
| <what was decided> | <the reason> |
