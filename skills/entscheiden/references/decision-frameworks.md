# Decision-Frameworks — Templates & Anker

> Referenz zu `/entscheiden`. Nur laden, wenn eine Stage tiefer gebraucht wird.

## Reversibilität × Tragweite → Aufwand (Kalibrierung)
| | reversibel (Zwei-Wege-Tür) | schwer umkehrbar (Einweg-Tür) |
|---|---|---|
| **geringe Tragweite** | sofort entscheiden, kein Prozess | Pre-Mortem + Kill-Criteria, dann GO |
| **hohe Tragweite** | billiger Test zuerst, dann entscheiden | **volle 6-Stage-Pipeline + `strategie-analyst`** |

Regel: Rigor an Reversibilität koppeln. Eine Zwei-Wege-Tür zu vergauntletten ist Verschwendung;
eine Einweg-Tür im Bauchgefühl zu nehmen ist fahrlässig.

## Pre-Mortem (Template)
> „Es ist [Datum + 12 Monate]. [Entscheidung] wurde umgesetzt und ist gescheitert. Warum?"
- Liste 3-5 *konkrete* Todesursachen (nicht „Markt war schlecht" → „ICP hatte kein Budget in Q3").
- Pro Ursache: Frühwarn-Signal + ob es messbar ist → speist Kill-Criteria.

## Tradeoff-Matrix (ehrlich)
| Option | Upside | **Was du aufgibst** | Reversibel? | Tragende Annahme |
|---|---|---|---|---|
| A | … | … | ja/nein | … |
| B | … | … | ja/nein | … |
| nichts tun | Status quo | Opportunitätskosten | — | … |
Jede Zeile MUSS eine „Was du aufgibst"-Spalte haben — sonst ist es ein Pitch, keine Entscheidung.

## Second-Order-Fragen
- Welche *Anreize* ändern sich (für dich, Team, Kunden, Wettbewerber)?
- Welche *Abhängigkeit* entsteht neu (Vendor, Person, Technologie)?
- Was tut die Gegenseite als *Reaktion* auf Zug 1 (Zug 2)?
- Was wird *schwerer/leichter*, das du nach dieser Entscheidung noch tun willst?

## Blast-Radius (Skala)
- **Wer** betroffen: nur ich / Team / Kunden / Reputation / Recht.
- **Wie schlimm**: Ärger ↔ existenzbedrohend.
- **Reversibilität des Schadens**: billig undo ↔ irreversibel. Einweg-Schaden hebt die Beweislast.

## Kill-Criteria (Template)
„Wir stoppen/kehren um, WENN **[messbare Metrik] [Operator] [Schwelle] bis [Datum]**."
- Muss *vor* dem Commitment stehen und *messbar* sein. Beispiele: „< 2 zahlende Pilotkunden bis 8 Wochen",
  „CAC > 3× erwartetem ACV nach 30 Leads", „Burn übersteigt X ohne Signal Y".

## Option-Tree (gegen das falsche Entweder-Oder)
Immer mindestens einfügen: **(0) nichts tun / Status quo** · **(1) billiger reversibler Test zuerst** ·
dann die „großen" Optionen. Die meisten binären Entscheidungen sind in Wahrheit 3-5-fach.

## Verdikt-Block (Ausgabe-Format)
```
DECISION:      GO | NO-GO | CONDITIONAL-GO(<Bedingung>) | DEFER(<bis was>)
REVERSIBILITÄT: Einweg-Tür | Zwei-Wege-Tür
TRAGENDE ANNAHMEN: <1-3, je mit VERIFIED/ASSUMED/UNKNOWN>
KILL-CRITERIA: <messbare, vor-festgelegte Abbruch-Bedingungen>
WIDERLEGT MICH: <was diese Empfehlung kippen würde>
BILLIGSTER TEST: <das Experiment, das die Kern-Annahme vor der großen Wette de-riskt>
```
