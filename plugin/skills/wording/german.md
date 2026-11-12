# German

German texts are written in German, never translated: German word order, the words a German speaker
uses for the meaning. Every rule of `rules.md` holds. This file adds what is German only.

## Address

The project decides du or Sie, and every German text of the project uses that one form. A text that
needs no address leaves it out (`Gespeichert.` rather than `Du hast gespeichert.`). The capital
`Du` is not used in an interface text.

## Typography

After DIN 5008:

- **A space before a unit and before %**: `20 m`, `5 %`, `3 GB`. A non-breaking space where the
  medium supports it.
- **„…“ as quotes**, and ‚…‘ inside them. Never "…" or »…«.
- **× for a count of things**: `3 × Brot`. Never `3x` or `3 *`.
- **… as one character** for an ellipsis, with a space before it when it stands for a missing word
  or a running action: `Der Zahlungslink wird erstellt …`.
- **Numbers**: a comma as the decimal sign, `2,5 km`. A time with a colon, `14:30 Uhr`. A date as
  `12.11.2026` or `12. November 2026`, one form per project.

## Words

- **Verbs over nouns**: `Gespeichert.`, not `Die Speicherung ist erfolgt.` A noun ending in -ung,
  -heit or -keit is a sign to look for the verb.
- **The platform's own German word** before an English one, as the platform's German localisation
  uses it: `Konto`, not `Account`, when the platform says Konto. The project's term list names
  these.
- **Compounds** are written as one word, or with a hyphen where a part is a name, an abbreviation or
  an English word: `Benutzerkonto`, `E-Mail-Adresse`, `Login-Code`. Never with a space between the
  parts.
- **Neutral wording** without a gender star, colon or capital I: a neutral noun (`Teammitglied`,
  `Person`, `alle, die geholfen haben`), a plural, or a sentence turned around the person, wherever one
  reads naturally.

## Controls

A button or menu entry is an infinitive with its object: `Alles nehmen`, `Dateien hochladen`,
`Backup löschen`. Never an imperative (`Nimm alles`) and never a noun (`Abgabe`).

## Pairs

- Fails: `Klicken, um Dateien hochzuladen.` as a tooltip on a clear control
- Passes: the control label `Dateien hochladen` without a tooltip
- Fails: `Du bekommst {amount}x {item}.`
- Passes: `Du bekommst {amount} × {item}.`
- Fails: `Noch {time}, {distance}m bis zum Ziel`
- Passes: `Noch {time}, {distance} m bis zum Ziel`
- Fails: `Das Ziel "{objective}" ist geschafft.`
- Passes: `Das Ziel „{objective}“ ist geschafft.`
- Fails: `Los! Die Runde läuft.`
- Passes: `Los. Die Runde läuft.`
