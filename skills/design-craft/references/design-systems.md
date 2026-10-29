# Design-Systeme — Brief → offizielles Paket

> WENN das Brief nach einem etablierten System klingt: das **offizielle** Paket installieren und nutzen —
> nicht seine CSS von Hand nachbauen, nicht seine Tokens importieren und dann 90% überschreiben.
> **Ein System pro Projekt.** Nur relevant beim Projekt-Track (nicht in CSP-Artifacts ohne Build).

## 1. Reach for a real system (Brief → Paket)

| Brief liest sich wie … | Offizielles Paket |
|---|---|
| Microsoft / Fluent / Office-Ökosystem | `@fluentui/react-components` |
| Android / Google / „Material" | `@material/web` (Material 3) |
| IBM / Enterprise-Data | `@carbon/react` |
| Shopify / Commerce-Admin | Polaris (`@shopify/polaris`) |
| Atlassian / Jira-Stil | Atlaskit |
| GitHub-Stil | Primer (`@primer/react`) |
| UK-Behörde | `govuk-frontend` |
| US-Behörde | `uswds` |
| „schnell, vertraut, bootstrappy" | Bootstrap 5.3 |
| Radix-Primitives + Theme | Radix Themes |
| „shadcn-Look", Tailwind-nativ | shadcn/ui (auf Tailwind v4) |
| generisch utility-first | Tailwind v4 |

**Zwei Ehrlichkeitsregeln:**
1. Liest sich das Brief als eines dieser Systeme → offizielles Paket installieren, nicht die CSS nachbauen.
2. Nicht Tokens eines Systems importieren und dann fast alles überschreiben. Ein System pro Projekt.

## 2. Ästhetiken, die *keine* Systeme sind

Glassmorphism, Bento, Brutalism, Editorial, Dark-Tech, Aurora, Kinetic-Type, Apple-„Liquid Glass" —
das sind **Welten** (`aesthetic-worlds.md`), keine installierbaren Systeme. Ehrliche Umsetzung:
- Es gibt **kein** offizielles `liquid-glass.css` — Web-Versionen sind Approximationen, so labeln.
- Glass/Blur nur als *spezifischer Effekt*, nicht als Deko-Default (→ `craft-floor.md §2`).
- Bento als Layout-Familie, nicht als Struktur-Krücke (Cell-Count-Regel, `craft-floor.md §4`).

## 3. Reality-Anchor

Beim Bau echte Doc-URLs/npm-Namen verwenden, nie erfundene Paketnamen. Bei Unsicherheit über die
aktuelle API → Context7-MCP oder offizielle Docs prüfen, nicht raten.

---
*Adaption (Prosa) aus Leonxlnx/taste-skill (MIT). Siehe `../CREDITS.md`.*
