---
description: Internet-Speedtest ausführen (Download/Upload/Ping)
---

Führe den Internet-Speedtest aus:

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/speedtest/run.sh $ARGUMENTS
```

Das Script misst via **Cloudflare** (Edge Frankfurt) und gibt Ping/Download/Upload
bereits menschenlesbar aus — Ergebnis einfach **kurz** zusammenfassen.

Wichtig:
- Der Test misst die Anbindung des **Servers/VPS**, auf dem Claude läuft — *nicht*
  die Internetleitung des Nutzers zu Hause.
- `speedtest.net` ist auf Server-IPs oft unbrauchbar (GeoIP verortet die IP falsch →
  ferne Server in Bulgarien, >450 ms Ping, verfälschte Werte). Darum Cloudflare.
- Mit `--classic` als Argument läuft zusätzlich der alte speedtest.net-Test
  (nur zum Vergleich).
