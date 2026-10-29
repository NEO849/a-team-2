# dnsx-Output & Cross-Run-Merge — Recipes

## Achtung: ANSI-Farbcodes in älteren/manuellen dnsx-Läufen
`run_target_recon.sh` ruft dnsx mit `-silent -o resolved.txt` auf → reine
Hostnamen-Liste, ein Name pro Zeile. Ältere oder manuell ausgeführte dnsx-Läufe
(ohne `-silent`/mit Terminal-Farbausgabe) landen dagegen so in der Datei:
```
hostname [␛[35mA␛[0m] [␛[32m1.2.3.4␛[0m]
```
Feldtrenner und Regex-Matches brechen lautlos, wenn diese Escape-Codes
übersehen werden.

### Sniff zuerst
```bash
grep -qP '\x1b\[' resolved.txt && echo "ANSI-farbig — erst strippen"
```

### Strippen (Idiom aus `run_target_recon.sh`'s cdncheck-Schritt übernommen)
```bash
sed 's/\x1b\[[0-9;]*m//g' resolved.txt > resolved_clean.txt
```

## Plain-Variante (Standardfall, `-silent -o`)
```bash
sort -u resolved.txt
```

## Farbige Variante nach Hostname/IP trennen
```bash
sed 's/\x1b\[[0-9;]*m//g' resolved.txt | awk -F'[][ ]+' '{print $1, $4}'
```
(`-F'[][ ]+'` behandelt Klammern und Leerzeichen als Multi-Trennzeichen.)

## dnsx JSON-Lines
```bash
# Mit jq (sauber):
jq -r '.host' dnsx_records.json
# Ohne jq-Abhängigkeit (Fallback):
grep -oE '"host":"[^"]*"' dnsx_records.json | cut -d'"' -f4
```

## Generalisiertes Merge/Dedupe über mehrere Recon-Läufe
Kernzeile aus `merge_best_recon.sh`, hier als eigenständiges, auf beliebige
Dateien anwendbares Muster (nicht an das feste `run_*/`-Kategorie-Schema des
Scripts gebunden):
```bash
awk 'NF' lauf1.txt lauf2.txt lauf3.txt | sort -u > merged.txt
```
Entfernt Leerzeilen, führt beliebig viele Dateien zusammen, dedupliziert.

## Weiterführend
"Was ist neu seit dem letzten Lauf" (statt nur Merge) ist ein Diff, kein Merge
→ `advanced-techniques.md`.
