# Examples

Texts of a real project, reworked with this standard, with the project's own names replaced by
plain ones. Each shows the text before, the text after and the rules that changed it. A text marked
"unchanged" passed as it was, and the reason says why.

## Changed

| Before | After | Rules |
| --- | --- | --- |
| `{player} hat kein verknüpftes Konto. Der Login hätte diesen Spieler abweisen müssen.` | `{player} hat kein verknüpftes Konto.` | R1 |
| `Offener Kauf {reference}: {days} Tage, begonnen am {since}. Es wurde kein Zahlungslink erstellt. Der Spieler hat abgebrochen, bevor er einen angefordert hat.` | `Offener Kauf {reference}: {days} Tage, seit {since}, ohne Zahlungslink.` | R1, R2, R6, R10 |
| `Das Limit ist auf {limit} gesetzt. Die Änderung ist gespeichert.` | `Das Limit ist jetzt {limit}.` | R2, R12 |
| `Ziel {key} ist von Hand abgeschlossen. Es zahlt aus, was gesammelt wurde, nicht das ganze Budget.` | `Ziel {key} ist von Hand abgeschlossen. {paid} ausgezahlt.` | R1, R4 |
| `Ein Tod kostet dich {points} Punkte.` | `−{points} Punkte` | R1, R3 |
| `Das Spiel kann gerade nicht beginnen. Versuch es später noch einmal.` | `Kein Spiel möglich: {reason}.` | R4, R6 |
| `Das ist fehlgeschlagen. Es wurde nichts geändert. Das Log nennt den Grund.` | `Fehlgeschlagen: {cause}. Nichts geändert.` | R3, R4 |
| `Lange ist nichts passiert. Die Zone schrumpft jetzt langsam.` | `Die Zone schrumpft langsam.` | R1 |
| `Dein Teampartner ist vor dem Countdown nicht beigetreten.` | `Dein Teammitglied ist vor dem Countdown nicht beigetreten.` | R10 |
| `Du bist nicht für das Turnier registriert. Registriere dich zuerst auf der Website.` | `Du bist nicht für das Turnier angemeldet. Melde dich auf der Website an.` | R6, R8 |
| `Das Netzwerk ist falsch konfiguriert. Niemand kann beitreten, bis ein Admin das behebt.` | `Das Netzwerk ist falsch konfiguriert.` | R1 |
| `Update lädt. Beim ersten Mal dauert es länger.` | `Update lädt.` | R1 |
| `Einladung an {partner} gesendet. Euer Team ist komplett, sobald die Einladung angenommen ist.` | `Einladung an {partner} gesendet.` | R1 |
| `Die Anmeldung ist geschlossen, solange ein Spiel läuft. Sie öffnet, wenn das Spiel endet.` | `Die Anmeldung ist geschlossen, bis das Spiel endet.` | R2, R3 |
| `Dein Account ist getrennt.` | `Dein Konto ist nicht mehr verknüpft.` | R8, R12 |
| `{mode} is the active mode. A switch to it is only a try again after a failed switch.` | `{mode} is already active.` | R1 |
| `agent.token is empty. The service needs it to send requests to the agent. The setup script writes it.` | `agent.token is empty. Run the setup script.` | R1, R5 |
| `This account has no security key or authenticator app yet. A key is required. Add one and try again.` | `This account has no security key or authenticator app. Add one.` | R1, R6 |
| `That sign-in started in another browser, finished already, or waited ten minutes without an answer. Start it again.` | `That sign-in is no longer open. Start it again.` | R1 |
| `Run asked for` | `Run requested` | R6 |

The sign-in text drops three causes because the code cannot tell which of them happened. A cause the
code does know stays (R4).

## Unchanged

| Text | Why it passes |
| --- | --- |
| `Der Server kann deinen Fortschritt nicht laden. Komm in ein paar Minuten wieder.` | It says what happened and what the reader does. |
| `Der Code ist falsch oder abgelaufen. Melde dich neu an, dann bekommst du einen neuen.` | The next step is shown nowhere else (R5). |
| `Das Verknüpfen hat nicht geklappt. Ein Admin weiß Bescheid. Versuch es in ein paar Minuten.` | "Ein Admin weiß Bescheid" says what happened and spares the reader a report. |
| `Wähle die Region, aus der du spielst. Jede Zeit erscheint in ihrer Zeitzone.` | The second sentence says what the choice does. |
| `Sends a private message to a player on the network.` | A help text: the reader asked for the explanation (R1). |
| `Too many wrong codes. Try again after {until}.` | The value replaces the stock phrase (R4). |
| `Alles nehmen` | A verb and its object (R7). |
| `Verschwindet in {left}` | A state, as short as the place allows. |
