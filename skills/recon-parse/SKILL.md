---
name: recon-parse
description: >
  Ad-hoc awk/Unix-Cookbook zum Filtern, Vergleichen und Deduplizieren bereits
  vorliegender Netzwerk-Recon-Rohdaten (nmap-gnmap, httpx, dnsx, ffuf/gobuster) —
  die interaktive Ebene ÜBER festen Pipeline-Scripts. Deckt reale
  Format-Eigenheiten ab: httpx-Feldzahl wechselt zwischen Läufen (Positions-Parsing
  bricht), dnsx-Ausgaben können ANSI-Farbcodes enthalten. Enthält fortgeschrittene
  Techniken: Zwei-Pass-awk als Join-/Diff-Ersatz für unsortierte Dateien,
  Content-Length-Clustering gegen ffuf/gobuster-Soft-404-Rauschen,
  Frequenz-/Ausreißer-Filterung in httpx-Listen. Kein Ersatz für eine feste
  Scan-Pipeline oder die Scan-Methodik selbst — nutze diesen Skill, wenn eine
  bereits vorhandene Recon-Datei ad-hoc ausgewertet werden soll.
  Trigger "zeig mir alle 403 mit cloudflare tech", "dedupe ips aus zwei gnmap
  läufen", "was ist neu seit dem letzten scan", "awk trick für httpx output",
  "parse die gnmap datei".
allowed-tools: Bash, Read, Grep
---

# Recon-Parse — Ad-hoc Text-Processing für Recon-Rohdaten

Cookbook, keine Scan-Ausführung: Dieser Skill wertet bereits vorliegende
Recon-Dateien aus (filtern, vergleichen, deduplizieren, kreuzreferenzieren). Er
scannt nichts selbst und stellt keine eigenen Live-Requests.

## Wann dieser Skill greift

Sobald eine konkrete, bereits vorhandene Recon-Rohdatei ad-hoc ausgewertet werden
soll — z.B. "zeig mir alle 403 mit Cloudflare-Tech", "dedupe IPs aus zwei
gnmap-Läufen", "was ist neu seit dem letzten Scan", "welche httpx-Zeilen haben
Content-Length X". Jede Anfrage hat andere Zielspalten/Filterkriterien — die
Rezepte unten sind Bausteine zum Anpassen, keine fertigen Reports.

**Abgrenzung zu Nachbar-Skills/Scripts:**
- Eine feste Pipeline-Stufe mit festen Feldpositionen/Scoring für EINE Scan-Stufe —
  nicht duplizieren; wenn die Frage "wie scort meine Pipeline das?" ist, dort
  nachsehen, nicht hier neu bauen.
- Scan-Methodik (WAS/WANN gescannt wird) gehört in einen eigenen Recon-Skill/Playbook.
  Dieser Skill ist WIE eine bereits gescannte Textdatei danach zerlegt wird.
- Ein festverdrahtetes Dedupe/Merge-Script für ein eigenes Lauf-Schema bleibt
  projektspezifisch. `references/dnsx-and-merge.md` liefert das generalisierte,
  auf beliebige Dateien anwendbare Muster dahinter.

## Eingabeformate

| Format | Typische Quelle | Referenz |
|---|---|---|
| nmap gnmap (`-oG`) | `nmap -oG` | `references/nmap-gnmap.md` |
| httpx Klammer-Text | `httpx`-Ausgabe | `references/httpx-parsing.md` |
| dnsx JSONL / Flat / ANSI | `dnsx`-Ausgabe | `references/dnsx-and-merge.md` |
| ffuf/gobuster Rohtext | Tool-Standardformat | `references/ffuf-gobuster.md` |
| Cross-Run-Diff/Join | jedes obige Format | `references/advanced-techniques.md` |

## Faustregeln (vor jedem Rezept)

1. **Erst hinsehen, dann parsen:** `head -3 datei | cat -A` — zeigt versteckte
   ANSI-Escapes/Steuerzeichen, bevor ein Feldtrenner angenommen wird.
2. **Leerzeilen killen, dann dedupe:** `awk 'NF'` vor jedem `sort -u`.
3. **Bei Klammerformaten (httpx):** Wenn die Feldzahl zwischen Zeilen schwanken
   kann, per Regex/Klammerpaar matchen (`grep -oE '\[[^]]*\]'`), nicht mit festem
   `$N` — siehe `references/httpx-parsing.md`, Feldzahl-Sniff zuerst.

## Cookbook-Pointer

- Siehe `references/nmap-gnmap.md` WENN eine `.gnmap`-Datei nach Hosts/Ports/
  Services gefiltert werden soll.
- Siehe `references/httpx-parsing.md` WENN eine httpx-Ergebnisdatei nach Status/
  Tech/Titel gefiltert, gezählt oder auf Ausreißer geprüft werden soll.
- Siehe `references/dnsx-and-merge.md` WENN dnsx-Output geparst oder mehrere
  Recon-Läufe zusammengeführt werden sollen.
- Siehe `references/ffuf-gobuster.md` WENN Fuzzing-Rohtext nach echten Treffern
  gefiltert werden soll (Content-Length-Rauschen).
- Siehe `references/advanced-techniques.md` WENN es um Diff/Join zwischen zwei
  unsortierten Dateien oder Cross-Tool-Abgleich (httpx vs. nmap) geht.

## Caveats

- Die ffuf/gobuster-Rezepte basieren auf dem publizierten Tool-Standardformat,
  nicht auf einer im Repo vorgefundenen Beispieldatei — vor Nutzung mit `head -5`
  der tatsächlichen Ausgabe gegenprüfen.
- Cross-Tool-Abgleich (z.B. httpx-Tech vs. nmap-Service) liefert einen **Hinweis**,
  keinen Beweis — unterschiedliche Tools nutzen unterschiedliche
  Fingerprint-Vokabulare.
- Ergebnisse dieses Skills sind Kandidatenlisten/Leads für die weitere manuelle
  Prüfung, keine bestätigten Findings.
