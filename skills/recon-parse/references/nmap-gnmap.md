# nmap gnmap — Recipes

Quelle: `nmap_max.sh` erzeugt `-oA`/`-oG` (Standard-nmap-Grepable-Format). Zwei
Zeilentypen sind relevant:

```
Host: 1.2.3.4 ()  Status: Up
Host: 1.2.3.4 ()  Ports: 80/open/tcp//http///, 443/open/tcp//https///
```

Jeder Ports-Eintrag ist `port/state/proto/owner/service/rpcinfo/version`,
Komma-getrennt.

## Live-Hosts extrahieren
```bash
awk '/Up$/{print $2}' scan.gnmap
```
(1:1 aus `nmap_max.sh` übernommen.)

## Alle offenen Ports, global dedupliziert
```bash
grep -oE '[0-9]+/open' scan.gnmap | cut -d/ -f1 | sort -un
```

## Service+Version-Tabelle je offenem Port
```bash
grep -oE '[0-9]+/open/[^,]*' scan.gnmap | awk -F/ '{printf "%-8s %-16s %s\n", $1, $5, $7}'
```
(Verifiziertes Muster aus `nmap_max.sh`.) Spalten: Port, Service, Version.

## Host → offene Ports (statt globaler Liste)
```bash
awk -F'Ports: ' '/Ports:/{host=$0; sub(/ .*/,"",host); sub(/^Host: /,"",host);
  n=split($2,ports,", "); for(i=1;i<=n;i++){split(ports[i],p,"/"); print host, p[1]}}' scan.gnmap
```
Gibt `host port` je Zeile aus — Grundlage für Cross-Referenzen (siehe
`advanced-techniques.md`).

## Nur Hosts filtern, bei denen ein bestimmter Port offen ist (z.B. 443)
```bash
awk '/Ports:/ && /443\/open/{print $2}' scan.gnmap
```

## Weiterführend
Diff zwischen zwei gnmap-Läufen (neue offene Ports seit letztem Scan) →
`advanced-techniques.md`.
