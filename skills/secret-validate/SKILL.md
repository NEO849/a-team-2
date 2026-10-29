---
name: secret-validate
description: >
  Read-only Live-Confirmation für gefundene Credentials/API-Keys (aus JS-Bundle,
  Sourcemap, .env-Leak, git-Historie). Bestätigt klinisch OB ein Key LIVE ist und
  WELCHEN Scope er hat — ohne destruktive/state-ändernde Aktion. Schließt die Lücke
  zwischen "Key gefunden" (≤45% Confidence) und "Key live + Scope bestätigt"
  (Server-Confirm) für unsere READ-demonstrierbare Submit-Bar. Unterstützt GitHub,
  GitLab, Postman, Slack, Anthropic, OpenAI, npm, Datadog (Header-basiert,
  stdlib-only, Default Dry-Run); AWS/JWT als dokumentierte Sonderfälle. Hard-Gates:
  read-only, minimale Calls, detectability-getaggt, nie AWS-root, kein Submit ohne
  ausdrückliches User-OK. Trigger "/secret-validate <provider>", "secret validate",
  "ist der key live", "validate api key", "key live check", "confirm leaked credential".
allowed-tools: Bash, Read
---

# Secret-Validate — Read-Only Credential Confirmation

Self-authored (kein fremder Code). Verwandelt einen gefundenen Key in einen
server-bestätigten Befund — **ohne** eine einzige schreibende/teure Aktion.

## Harvest-Vorstufe — TruffleHog
Vor diesem Skill steht das Finden+Vor-Filtern. **`trufflehog`** klassifiziert 800+ Secret-Typen und **verifiziert live** (`--only-verified` killt False-Positives):
```bash
trufflehog github --org <ORG> --only-verified --json 2>/dev/null     # nur in-scope Org
trufflehog filesystem <sourcemap-dump-dir> --only-verified --json
trufflehog git file://<lokaler-klon> --only-verified --json          # Commit-History
```
Arbeitsteilung: TruffleHog = Breite+erste Liveness (eigene Verifier, deckt Slack/Notion/Confluence). `validate.py` = klinischer Einzel-Confirm + **Scope-Auslesen** (`X-OAuth-Scopes` = Severity) für den finalen Report-Beleg. Ergänzend Commit-History-Suche (z.B. über eine Code-Search-Engine) für gelöschte Keys. ⛔ TruffleHog-Verify ist Live-HTTP — bei automatisierter Ausführung ggf. vom eigenen Setup geblockt, dann manuell/user-initiiert ausführen.

## Wann nutzen
- Nach JS-/Sourcemap-/`.env`-Harvest **oder TruffleHog-Hit** hat einen Key-Kandidaten geliefert.
- Ein Befund hängt an "ist diese Cred echt?" — wir wollen Server-Confirm statt Spekulation.
- Vor jedem Report, der einen Key als Impact nennt (Confidence nie auf bloßem Fund-Verdacht aufblasen).

## ⛔ Hard-Gates (nicht verhandelbar)
1. **Read-only.** Nur Identity/Validate-Endpoints. NIE `chat.postMessage`, `files.upload`,
   `repo`-Writes, Deploys, Rotation, Delete. Das Skript erlaubt nur die Allowlist.
2. **Nur in-scope Keys.** Validiere ausschließlich Credentials, die zum autorisierten
   Target gehören. Fremde Keys aus Sammel-Leaks NICHT anfassen.
3. **Detectability.** Jeder Probe-Output trägt `detectability` — der Owner sieht den
   Call evtl. im Audit-Log (z.B. AWS CloudTrail `GetCallerIdentity`, Datadog-Audit).
   Minimal-invasiv: 1 Validate-Call, dann stoppen.
4. **AWS-Root NIE.** `:root`-ARN niemals validieren. AWS generell nur via aws-cli-Note unten.
5. **Confidence erst nach Live-Confirm**, **kein Submit ohne ausdrückliches User-OK**.
6. **Live-Exec nur mit Bedacht.** Der Validate-Call ist Live-HTTP — in einer automatisierten
   Umgebung ggf. durch ein eigenes Sicherheitsnetz geblockt; dann manuell/user-initiiert ausführen.

## How to Run
```bash
SV=${CLAUDE_SKILL_DIR}/validate.py

python3 $SV --list                                   # Allowlist + Endpoints
echo 'ghp_xxx' | python3 $SV github                  # DRY-RUN (zeigt nur den Plan)
echo 'ghp_xxx' | python3 $SV github --confirm        # read-only Live-Confirm
python3 $SV slack --token 'xoxb-...' --confirm
```
Default = **Dry-Run** (kein Request). `--confirm` sendet genau einen read-only Call.
Pure stdlib (urllib), keine Dependencies, keine Drittanbieter-Skripte.

## Output-Schema (maschinenlesbar)
```json
{ "status": "verified_live|verified_dead|validation_failed_transient",
  "provider": "...", "http_status": 200, "token_scopes": "<X-OAuth-Scopes>",
  "detectability": "low|medium", "evidence_snippet": "<=300 chars" }
```
`token_scopes` (GitHub `X-OAuth-Scopes`) entscheidet Impact: `repo` = Write auf alle
erreichbaren Repos; `admin:org` = Org-Admin. Scope = Severity, nicht bloße Liveness.

## Provider-Matrix (alle read-only)
| Provider | Endpoint | Header | Liveness-Signal | Detect |
|---|---|---|---|---|
| github | GET /user | `Authorization: token` | 200 + `X-OAuth-Scopes` | low |
| gitlab | GET /api/v4/user | `PRIVATE-TOKEN` | 200 | low |
| postman | GET /me | `X-Api-Key` | 200 → user obj | low |
| slack | POST auth.test | `Bearer` | `{"ok":true}` | low |
| anthropic | GET /v1/models | `x-api-key`+ver | 200 | low (Console) |
| openai | GET /v1/models | `Bearer` | 200 / 429=live | low (dashboard) |
| npm | GET /-/whoami | `Bearer` | 200 → username | low |
| datadog | GET /api/v1/validate | `DD-API-KEY` | 200 | low (audit) |

### AWS (Sonderfall — NICHT im Skript)
Read-only Identitäts-Check, nur mit aws-cli/eigenem boto3, **nie für `:root`**:
```bash
aws sts get-caller-identity   # gibt Account-ID + ARN + UserId; CloudTrail loggt es
```
ARN-Lesart: `:user/`=IAM-User (breit), `:assumed-role/`=temp (eng), `:root`=**nicht testen**.

### JWT (kein Netz-Call nötig)
Header/Payload base64url-dekodieren → `alg` (none/HS*/RS*), `kid`/`jku`/`x5u`
(Injection-Targets), `exp`, Privileg-Claims. Für tiefere Krypto-/Protokoll-Analyse
an einen entsprechenden Spezialisten-Skill/Agenten weiterreichen, falls vorhanden.

## Pitfalls
- **Liveness ≠ Bug.** Ein hardcodierter Client-Key im SPA-Bundle ist oft so
  vorgesehen (Working-As-Intended) — Kill-Test `ohne==mit` (funktioniert der
  Zugriff auch ohne den Key genauso?). Liveness liefert Server-Confirm, der
  **Impact** muss separat bewiesen werden.
- **429 = live** (Quota erschöpft), nicht tot.
- **Datadog-Region** variiert (`.eu`, `.us3`) — bei 403 Region prüfen, nicht "tot".
- **Slack 200 mit `ok:false`** = tot (Skript behandelt das).
- Mehr als 1 Call pro Key = unnötige Detectability. Stoppen nach Confirm.

## Verification
- `status: verified_live` + `http_status` + `evidence_snippet` = Server-Confirm-Beleg.
- Scope dokumentieren (entscheidet Severity).
- Danach: Impact-Pfad bauen (was liest/kann der Key wirklich?) → erst dann Report-Draft.
