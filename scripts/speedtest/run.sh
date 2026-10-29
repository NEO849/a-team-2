#!/usr/bin/env bash
# Internet-Speedtest via Cloudflare (Down/Up/Ping).
# Misst die Anbindung DIESES Servers/VPS, nicht die Heimleitung des Nutzers.
#
# Warum Cloudflare statt speedtest.net: Die VPS-IP wird von speedtest.net
# geografisch falsch verortet (→ ferne Server in Bulgarien, 1200 km, >450 ms Ping),
# was die Werte massiv verfälscht. Cloudflare hat einen Edge in Frankfurt (~1-2 ms)
# und liefert daher die echte Bandbreite.
#
# Optional: "--classic" führt zusätzlich den alten speedtest.net-Test aus.
set -euo pipefail

JAR="$(mktemp)"
UA="Mozilla/5.0 (X11; Linux x86_64) speedtest"
BASE="https://speed.cloudflare.com"
trap 'rm -f "$JAR"' EXIT

cf() { curl -s -A "$UA" -c "$JAR" -b "$JAR" "$@"; }

echo "=== Internet-Speedtest (Cloudflare) ==="

# Edge-Standort (colo) + Ping aus einem kleinen Request.
meta="$(cf -D - -o /dev/null "$BASE/__down?bytes=1000" 2>/dev/null || true)"
colo="$(echo "$meta" | awk -F': ' 'tolower($1)=="colo"{gsub(/\r/,"",$2);print $2}')"
city="$(echo "$meta" | awk -F': ' 'tolower($1)=="city"{gsub(/\r/,"",$2);print $2}')"

# Ping = TCP-Connect-Zeit (RTT), Mittel aus 4 Messungen.
ping_sum=0; n=4
for _ in $(seq $n); do
  t="$(cf -o /dev/null -w '%{time_connect}' "$BASE/__down?bytes=0" 2>/dev/null || echo 0)"
  ping_sum="$(awk -v a="$ping_sum" -v b="$t" 'BEGIN{print a+b}')"
done
ping_ms="$(awk -v s="$ping_sum" -v n="$n" 'BEGIN{printf "%.0f", (s/n)*1000}')"

# Download: 80 MB.
dl="$(cf -o /dev/null -w '%{speed_download}' "$BASE/__down?bytes=80000000" 2>/dev/null || echo 0)"
dl_mbit="$(awk -v b="$dl" 'BEGIN{printf "%.1f", b*8/1000000}')"

# Upload: 50 MB.
ul="$(head -c 50000000 /dev/zero | cf -o /dev/null -w '%{speed_upload}' --data-binary @- "$BASE/__up" 2>/dev/null || echo 0)"
ul_mbit="$(awk -v b="$ul" 'BEGIN{printf "%.1f", b*8/1000000}')"

echo "Server:   Cloudflare ${colo:-?} ${city:+($city)}"
echo "Ping:     ${ping_ms} ms"
echo "Download: ${dl_mbit} Mbit/s"
echo "Upload:   ${ul_mbit} Mbit/s"
echo "(Hinweis: misst die VPS-Anbindung, nicht die Heimleitung.)"

# Optionaler Klassik-Test gegen speedtest.net.
if [[ "${1:-}" == "--classic" ]]; then
  echo
  echo "=== Zusatz: speedtest.net (oft GeoIP-verzerrt auf Server-IPs) ==="
  "$(dirname "$0")/venv/bin/speedtest-cli" --secure 2>&1 || echo "speedtest.net-Test fehlgeschlagen."
fi
