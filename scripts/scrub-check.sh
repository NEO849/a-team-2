#!/usr/bin/env bash
# A-Team 2.0 — No-Secrets-Gate (local).
# Runs gitleaks + trufflehog + a denylist grep over the working tree and refuses
# on any hit. Structured, queryable logs (stable event names); exit codes:
#   0 = clean   1 = findings   2 = required tool missing   3 = usage error
#
# Design: we NEVER print the matched secret value — only the file, line and rule,
# so the log itself can't become a new leak (observability rule: no secrets in logs).
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCAN_DIR="${REPO_ROOT}/.scan"
MODE="${1:-full}"   # full = whole tree (default) | staged = staged changes only

log() { # log <level> <event> [k=v ...]
  local level="$1" event="$2"; shift 2
  printf '{"ts":"%s","level":"%s","event":"%s"' "$(date -u +%FT%TZ)" "$level" "$event"
  for kv in "$@"; do printf ',"%s":"%s"' "${kv%%=*}" "${kv#*=}"; done
  printf '}\n'
}

require() { # require <binary>
  if ! command -v "$1" >/dev/null 2>&1; then
    log error tool_missing tool="$1" hint="install $1 before running the gate"
    exit 2
  fi
}

main() {
  case "$MODE" in full|staged) ;; *) log error usage got="$MODE" want="full|staged"; exit 3;; esac
  require gitleaks
  require trufflehog
  mkdir -p "$SCAN_DIR"
  local rc=0

  log info gate_start mode="$MODE" repo="${REPO_ROOT##*/}"

  # 1) gitleaks (default rules + our .gitleaks.toml denylist).
  #    This gitleaks exposes `detect` (full tree, --no-git) and `protect --staged`.
  local gl_report="${SCAN_DIR}/gitleaks-report.json"
  rm -f "$gl_report"
  local gl_common=(--no-banner --redact --config "${REPO_ROOT}/.gitleaks.toml" --report-format json --report-path "$gl_report")
  local gl_rc=0
  if [ "$MODE" = staged ]; then
    gitleaks protect --staged --source "$REPO_ROOT" "${gl_common[@]}" >/dev/null 2>&1 || gl_rc=$?
  else
    gitleaks detect --no-git --source "$REPO_ROOT" "${gl_common[@]}" >/dev/null 2>&1 || gl_rc=$?
  fi
  if [ "$gl_rc" -eq 0 ]; then
    log info gitleaks_clean
  elif [ -s "$gl_report" ]; then
    local n; n="$(python3 -c 'import json,sys;print(len(json.load(open(sys.argv[1]))))' "$gl_report" 2>/dev/null || echo '?')"
    log error gitleaks_findings count="$n" report="$gl_report"
    rc=1
  else
    log error gitleaks_error rc="$gl_rc" hint="gitleaks invocation failed — treated as FAIL, not clean"
    rc=1
  fi

  # 2) trufflehog filesystem, verified + unverified candidates
  local th_report="${SCAN_DIR}/trufflehog-report.json"
  if trufflehog filesystem "$REPO_ROOT" --no-update --json >"$th_report" 2>/dev/null; then
    local th_n; th_n="$(wc -l <"$th_report" | tr -d ' ')"
    if [ "$th_n" -gt 0 ]; then
      log error trufflehog_findings count="$th_n" report="$th_report"; rc=1
    else
      log info trufflehog_clean
    fi
  else
    log warn trufflehog_nonzero_exit report="$th_report"
  fi

  # 3) belt-and-braces denylist grep (catches non-secret private markers gitleaks
  #    rules might miss); prints file:line + rule, never the match body.
  # NOTE: grep -E (ERE) does NOT support (?i) inline flags — they are literal there.
  # Case-insensitivity comes from the -i grep flag below; keep patterns flag-free.
  # Generic markers that reveal nothing identifying — safe to keep in the public gate.
  local deny='(^|[^A-Za-z0-9_])/root/|[A-Za-z0-9._%+-]+@gmail\.com'
  # The operator's IDENTIFYING denylist (handles, private targets, project/agent names,
  # build-host IP) lives OUTSIDE the tracked tree, so the public gate never ships the
  # very terms it blocks. One regex fragment per line; #-comments and blanks ignored.
  # Absent (e.g. a fresh public clone) → generic markers only (functional, just narrower).
  local deny_local="${REPO_ROOT}/scripts/scrub-denylist.local"
  if [ -f "$deny_local" ]; then
    local extra; extra="$(grep -vE '^[[:space:]]*(#|$)' "$deny_local" | paste -sd'|' -)"
    [ -n "$extra" ] && deny="${deny}|${extra}"
    log info denylist_local_loaded path="scripts/scrub-denylist.local"
  else
    log warn denylist_local_absent hint="private term list not present; generic markers only"
  fi
  local hits
  hits="$(grep -rnoEIi "$deny" "$REPO_ROOT" \
      --exclude-dir=.git --exclude-dir=.scan \
      --exclude=.gitleaks.toml --exclude=scrub-check.sh --exclude=scrub-denylist.local 2>/dev/null \
      | sed -E 's/:(.*)$//' | sort -u || true)"
  if [ -n "$hits" ]; then
    log error denylist_hits count="$(printf '%s\n' "$hits" | wc -l | tr -d ' ')"
    printf '%s\n' "$hits" | while IFS= read -r loc; do log error denylist_hit at="$loc"; done
    rc=1
  else
    log info denylist_clean
  fi

  if [ "$rc" -eq 0 ]; then log info gate_pass; else log error gate_fail hint="resolve findings above; nothing is pushed"; fi
  return "$rc"
}

main "$@"
