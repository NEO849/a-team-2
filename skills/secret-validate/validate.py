#!/usr/bin/env python3
"""
secret-validate — read-only live-credential confirmation.

Senior-Elite, self-authored (NOT copied from any third-party repo). Pure stdlib
(urllib), READ-ONLY requests only. Confirms whether a credential found in scope
(JS bundle, sourcemap, .env leak, git history) is LIVE and what its scope is —
WITHOUT any destructive or state-changing call.

Hard rules baked in:
  * Only the providers in PROVIDERS below are reachable (allowlist).
  * Every probe is a single read-only identity/validate endpoint (GET, or the
    vendor's documented auth-test POST that performs no mutation).
  * Default mode is DRY-RUN: prints what it WOULD send. Add --confirm to send.
  * AWS is intentionally NOT here (SigV4 + root-key risk) — use the aws-cli note
    in SKILL.md instead, and never validate a :root key you find.
  * 'detectability' is printed with every result — the owner may see the probe
    in their audit log. Validate only what you are authorized to test.

Usage:
  echo '<token>' | python3 validate.py <provider> [--confirm]
  python3 validate.py <provider> --token '<token>' [--confirm]
  python3 validate.py --list

Exit codes: 0 ok/handled, 2 usage error, 3 unsupported provider.
"""
import json
import sys
import urllib.request
import urllib.error

TIMEOUT = 10

# provider -> dict(method, url, headers(token)->{}, detectability, scope_note)
# url may contain {ws} for providers that need a workspace (atlassian).
PROVIDERS = {
    "github": dict(
        method="GET", url="https://api.github.com/user",
        headers=lambda t: {"Authorization": f"token {t}", "User-Agent": "secret-validate"},
        scope_header="X-OAuth-Scopes",
        detectability="low", scope="repo=write-all-accessible-repos; admin:org=org-admin"),
    "gitlab": dict(
        method="GET", url="https://gitlab.com/api/v4/user",
        headers=lambda t: {"PRIVATE-TOKEN": t},
        detectability="low", scope="api=full; read_api=read-only"),
    "postman": dict(
        method="GET", url="https://api.getpostman.com/me",
        headers=lambda t: {"X-Api-Key": t},
        detectability="low", scope="full read: collections, env vars, history"),
    "slack": dict(
        method="POST", url="https://slack.com/api/auth.test",
        headers=lambda t: {"Authorization": f"Bearer {t}"},
        detectability="low", scope="depends on token scopes (see response)"),
    "anthropic": dict(
        method="GET", url="https://api.anthropic.com/v1/models",
        headers=lambda t: {"x-api-key": t, "anthropic-version": "2023-06-01"},
        detectability="low (usage shows in Console)", scope="workspace API access"),
    "openai": dict(
        method="GET", url="https://api.openai.com/v1/models",
        headers=lambda t: {"Authorization": f"Bearer {t}"},
        detectability="low (usage shows in dashboard)", scope="org API access"),
    "npm": dict(
        method="GET", url="https://registry.npmjs.org/-/whoami",
        headers=lambda t: {"Authorization": f"Bearer {t}"},
        detectability="low", scope="read or publish (check /-/npm/v1/tokens)"),
    "datadog": dict(
        method="GET", url="https://api.datadoghq.com/api/v1/validate",
        headers=lambda t: {"DD-API-KEY": t},
        detectability="low (appears in DD audit log)",
        scope="api key validity (region may differ: .eu / .us3)"),
}


def probe(provider, token, confirm):
    p = PROVIDERS[provider]
    hdrs = p["headers"](token)
    redacted = {k: (v[:12] + "…" if len(v) > 16 else "***") for k, v in hdrs.items()}
    print(f"[plan] {p['method']} {p['url']}")
    print(f"[plan] headers: {redacted}")
    print(f"[info] detectability: {p['detectability']}")
    print(f"[info] scope-if-live: {p['scope']}")
    if not confirm:
        print("[dry-run] no request sent. add --confirm to validate (read-only).")
        return
    req = urllib.request.Request(p["url"], method=p["method"], headers=hdrs)
    if p["method"] == "POST":
        req.data = b""  # documented no-op auth test
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            body = r.read(4096).decode("utf-8", "replace")
            status = r.status
            scopes = r.headers.get(p.get("scope_header", "")) if p.get("scope_header") else None
    except urllib.error.HTTPError as e:
        status = e.code
        body = e.read(2048).decode("utf-8", "replace")
        scopes = None
    except Exception as e:  # noqa: BLE001 — transient/network
        print(json.dumps({"status": "validation_failed_transient",
                          "provider": provider, "error": str(e)}))
        return

    # Slack returns 200 with {"ok": false} for dead tokens — special-case it.
    live = status in (200, 429)
    if provider == "slack":
        try:
            live = json.loads(body).get("ok") is True
        except Exception:  # noqa: BLE001
            live = False

    result = {
        "status": "verified_live" if live else "verified_dead",
        "provider": provider,
        "http_status": status,
        "token_scopes": scopes,
        "detectability": p["detectability"],
        "note": "429 = live but rate/quota limited" if status == 429 else None,
        "evidence_snippet": body[:300],
    }
    print(json.dumps(result, indent=2))


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    if args[0] == "--list":
        for k, v in PROVIDERS.items():
            print(f"{k:10s} {v['method']:4s} {v['url']}  (detectability: {v['detectability']})")
        return 0
    provider = args[0].lower()
    if provider not in PROVIDERS:
        print(f"[error] unsupported provider '{provider}'. --list to see allowlist.", file=sys.stderr)
        return 3
    confirm = "--confirm" in args
    token = None
    if "--token" in args:
        token = args[args.index("--token") + 1]
    elif not sys.stdin.isatty():
        token = sys.stdin.read().strip()
    if not token:
        print("[error] no token (pipe it in or use --token).", file=sys.stderr)
        return 2
    probe(provider, token, confirm)
    return 0


if __name__ == "__main__":
    sys.exit(main())
