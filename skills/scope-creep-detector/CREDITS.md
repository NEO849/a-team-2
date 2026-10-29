# Credits

`scripts/scope_creep.py` und `references/scope-signals.md` sind unverändert
übernommen aus:

- **Quelle:** [Shubhamsaboo/awesome-llm-apps](https://github.com/Shubhamsaboo/awesome-llm-apps),
  `agent_skills/scope-creep-detector/`
- **Autor:** Matt Van Horn
- **Lizenz:** Apache-2.0
- **Static-Scan-Verdikt:** 🟢 SAFE-ADOPT (2026-08-21) — statischer Scan (semgrep +
  trufflehog + Heuristik) speziell für diesen Unterordner geprüft (nicht das
  Gesamt-Repo, dessen Aggregat-Score von unrelated Unterprojekten dominiert
  wird). Kein `shell=True`, keine Netzwerkaufrufe, keine Secrets in diesem Pfad.
  Manuell im Quellcode verifiziert: `subprocess.run(["git", "-C", repo, *args])`
  ohne Shell-Interpretation.

`SKILL.md` und `CREDITS.md` in diesem Verzeichnis sind eigenständig für dieses
System neu geschrieben (nicht aus der Quelle übernommen).
