# ffuf/gobuster — Recipes

**Caveat:** Die folgenden Rezepte basieren auf dem publizierten
Tool-Standardformat, nicht auf einer im Repo vorgefundenen Beispieldatei (keine
gefunden). Vor Nutzung `head -5` der tatsächlichen Ausgabe gegenprüfen und
Feldnamen/-trenner anpassen, falls abweichend.

## Typische Zeilenformate
```
# ffuf (Text-Output):
wortliste [Status: 200, Size: 1234, Words: 56, Lines: 12]
# gobuster (Text-Output):
/pfad (Status: 200) [Size: 1234]
```

## Content-Length extrahieren
```bash
# ffuf:
grep -oE 'Size: [0-9]+' out.txt | cut -d' ' -f2
# gobuster:
grep -oE '\[Size: [0-9]+\]' out.txt | tr -dc '0-9\n'
```

## Content-Length-Clustering gegen Soft-404-Rauschen (Kernrezept dieser Datei)
Idee: Bei Verzeichnis-/Wortlisten-Fuzzing antwortet der Server für die meisten
"nicht existierenden" Pfade mit derselben generischen Fehlerseite → gleiche
Content-Length. Statt jede Zeile manuell zu sichten, den häufigsten Wert als
Baseline identifizieren und nur Abweichungen als echte Kandidaten ausgeben.

```bash
# 1. Häufigkeitsverteilung der Size-Werte:
grep -oE 'Size: [0-9]+' out.txt | cut -d' ' -f2 | sort -n | uniq -c | sort -rn | head -5

# 2. Häufigster Wert (Beispiel: 4321) = wahrscheinlich Soft-404-Baseline.
#    Alles außerhalb davon ausgeben:
awk -F'Size: ' '{split($2,a," "); if (a[1] != 4321) print}' out.txt
```

Ein einzelner Ausreißer-Cluster reicht oft nicht — bei manchen Setups gibt es
2-3 generische Antwortgrößen (z.B. je nach Content-Type). Schritt 1 zeigt die
Top-5, alle davon als Baseline behandeln, nicht nur den einen häufigsten Wert.
