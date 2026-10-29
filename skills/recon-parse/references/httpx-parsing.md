# httpx Klammer-Format — Recipes

Reale httpx-Textausgaben im Repo zeigen **unterschiedliche Feldzahlen je nach
aktivierten Flags** — Beispiel drei tatsächlich vorgefundene Layouts:

```
URL [STATUS] [TITLE] [TECH,TECH,...]                      # 4 Felder
URL [STATUS] [] [] [IP] [TECH,...]                        # 6 Felder, zwei leer
URL [STATUS] [CONTENT-LENGTH] [cloudflare] [TECH,...]     # Feld 3 ist hier eine Zahl
```

**Konsequenz: positionelles `$N`-Parsen bricht zwischen Runs.** Immer zuerst die
Feldzahl der konkreten Datei prüfen, dann per Muster statt Position zugreifen.

## Schritt 1 — Feldzahl-Sniff (Pflicht vor jedem `$N`-Zugriff)
```bash
awk -F'[][]' '{print NF}' httpx_out.txt | sort -u
```
Mehrere unterschiedliche Werte → gemischtes Layout, nicht mit fixer Spalte
arbeiten.

## Robuste Klammer-Extraktion (positionsunabhängig)
```bash
grep -oE '\[[^]]*\]' httpx_out.txt
```
Liefert je Zeile die Klammerinhalte als Tokens — bei bekannter, gleichbleibender
Feldzahl dieser einen Datei mit `paste - - -` (Anzahl `-` = Feldzahl) wieder zu
Spalten zusammenfassen.

## Beispiel: 403 mit Cloudflare-Tech (matcht auf Inhalt, nicht Position)
```bash
grep -E '\[403\]' httpx_out.txt | grep -i cloudflare | cut -d' ' -f1
```

## Status-Code-Verteilung
```bash
grep -oE '\[[0-9]{3}\]' httpx_out.txt | tr -d '[]' | sort | uniq -c | sort -rn
```

## Tech-Stack einzeln zählen (letztes Klammerfeld ist meist die Tech-Liste)
```bash
grep -oE '\[[A-Za-z0-9 ,.]+\]$' httpx_out.txt | tr -d '[]' | tr ',' '\n' \
  | sort | uniq -c | sort -rn
```

## Frequenz-/Ausreißer-Erkennung (fortgeschritten)
Ziel: in einer großen Liste (z.B. 5000 Zeilen) die seltenen Title/Tech-
Kombinationen herausfiltern, statt alles manuell zu sichten. Zwei-Pass-Prinzip:
Pass 1 zählt Vorkommen eines Feldes, Pass 2 gibt nur Zeilen mit niedrigem Count
aus.
```bash
awk -F'[][]' '{print $3}' httpx_out.txt | sort | uniq -c | sort -n | head -20
```
Die Zeilen mit Count 1-2 am Anfang der sortierten Liste sind die Ausreißer —
oft ungewöhnliche Titel/Fehlermeldungen, die eine manuelle Prüfung wert sind.

## Weiterführend
Cross-Referenz httpx-Tech gegen nmap-Service (Mismatch = Hinweis, kein Beweis)
→ `advanced-techniques.md`.
