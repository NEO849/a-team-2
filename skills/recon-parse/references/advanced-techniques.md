# Advanced Techniques — Diff, Join, Cross-Referenz

TOC: 1) Grundmuster Zwei-Pass-awk · 2) Diff zwischen zwei Scan-Läufen ·
3) Cross-Referenz httpx vs. nmap

## 1. Grundmuster: Zwei-Pass-awk als Join-/Diff-Ersatz

`comm`/`join` brauchen sortierte Dateien mit dem Schlüssel in einer festen
Spalte. Recon-Dateien sind das selten (unsortiert, Schlüssel muss erst per
Regex extrahiert werden). Zwei-Pass-awk löst das ohne Vorsortierung:

```bash
awk 'FNR==NR{seen[$1]=1; next} !($1 in seen){print}' datei_a.txt datei_b.txt
```

- **Pass 1** (`FNR==NR` ist wahr solange die erste Datei gelesen wird): baut ein
  Array `seen[]` aus Spalte 1 von `datei_a.txt`.
- **Pass 2** (ab der zweiten Datei): gibt jede Zeile aus `datei_b.txt` aus,
  deren Spalte 1 NICHT im Array vorkommt.
- Ergebnis: alles, was in `datei_b.txt`, aber nicht in `datei_a.txt` steht.

Für "was ist gemeinsam" statt "was ist neu": Bedingung auf `($1 in seen)`
umdrehen.

## 2. Anwendung: Diff zwischen zwei Scan-Läufen

**Neue Live-Hosts seit letztem Lauf** (Eingabe: zwei Dateien, ein Hostname pro
Zeile, z.B. aus `dnsx-and-merge.md`):
```bash
awk 'FNR==NR{seen[$1]=1; next} !($1 in seen){print}' lauf_alt.txt lauf_neu.txt
```

**Neue offene Ports seit letztem Scan** (Eingabe: `host port`-Zeilen aus
`nmap-gnmap.md`'s Host→Port-Rezept, Schlüssel ist die Kombination — dafür beide
Felder zu einem Schlüssel zusammenfassen):
```bash
awk 'FNR==NR{seen[$1" "$2]=1; next} !(($1" "$2) in seen){print}' \
  hostports_alt.txt hostports_neu.txt
```

## 3. Anwendung: Cross-Referenz httpx-Tech vs. nmap-Service

**Caveat zuerst:** Ein Mismatch zwischen httpx-Tech-Fingerprint und
nmap-Service/Version-String ist ein **Hinweis**, kein Beweis — beide Tools
nutzen unterschiedliche Erkennungsheuristiken/Vokabulare (z.B. httpx erkennt
"nginx" über HTTP-Header, nmap über Port-Banner; beide können unabhängig
voneinander falsch liegen).

Join-Schlüssel ist die IP (httpx liefert sie im Klammer-Feld, wenn `-ip`
gesetzt war; nmap liefert sie in der `Host:`-Zeile):
```bash
# Pass 1: IP -> Tech aus httpx (Klammer-Feld mit IP identifizieren, hier Feld 4 als Beispiel)
awk -F'[][]' 'NR==FNR{ip=$8; tech=$10; map[ip]=tech; next}' httpx_out.txt /dev/null

# Kombiniert mit nmap-Service (aus nmap-gnmap.md Service-Tabelle, Spalte 2 = Host, Spalte 3 = Service):
awk -F'[][]' 'FNR==NR{map[$8]=$10; next}
  {if ($1 in map && map[$1] !~ $3) print $1, "httpx:"map[$1], "nmap:"$3}' \
  httpx_out.txt nmap_services.txt
```
Feldnummern (`$8`, `$10`, `$3`) sind Platzhalter — je nach tatsächlicher
Feldzahl der konkreten httpx-Datei anpassen (siehe Feldzahl-Sniff in
`httpx-parsing.md`, das gilt hier genauso).

## Weiterführend
Frequenz-/Ausreißer-Erkennung in httpx-Listen (verwandtes Zwei-Pass-Zählmuster,
aber anderer Zweck) ist in `httpx-parsing.md` erklärt, nicht hier dupliziert.
