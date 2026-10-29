#!/usr/bin/env python3
"""Skill-Autoren-Linter — durchgesetzt gegen skills/_shared/AUTHORING.md.

Read-only. Prueft jede skills/<name>/SKILL.md (optional commands/*.md) gegen den Kanon:
  - description <=1024 (WARN) / <=1536 hard-truncation (ERROR)
  - name-Regex ^[a-z0-9-]{1,64}$ (WARN bei Unterstrich/Non-ASCII), Reserved-Words anthropic/claude (ERROR)
  - fehlende description (ERROR)
  - body <500 Zeilen (WARN)
  - fehlende Trigger-Klausel (WARN)
  - kaputte relative references/*.md Links (ERROR)

Exit 0 = keine ERROR (Gate gruen). Exit 1 = mindestens ein ERROR.

Usage:
  python3 validate_skills.py                 # scannt ~/.claude/skills
  python3 validate_skills.py --commands      # zusaetzlich ~/.claude/commands
  python3 validate_skills.py --quiet         # nur Verstoesse + Summary
  python3 validate_skills.py --skills-dir /pfad
"""
import argparse
import os
import re
import sys

DESC_CAP = 1024          # Anthropic canonical description cap
DESC_HARD = 1536         # listing truncation (description + when_to_use)
BODY_MAX = 500           # SKILL.md body line budget
NAME_RE = re.compile(r'^[a-z0-9-]{1,64}$')
RESERVED = ('anthropic', 'claude')

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_SKILLS = os.path.normpath(os.path.join(HERE, '..', '..', 'skills'))
DEFAULT_COMMANDS = os.path.normpath(os.path.join(HERE, '..', '..', 'commands'))


def split_frontmatter(txt):
    """Return (frontmatter_str, body_str) or (None, txt) if no frontmatter."""
    if not txt.startswith('---'):
        return None, txt
    m = re.match(r'^---\n(.*?)\n---\n?(.*)$', txt, re.S)
    if not m:
        return None, txt
    return m.group(1), m.group(2)


def get_field_name(fm):
    m = re.search(r'^name:\s*(.+?)\s*$', fm, re.M)
    return m.group(1).strip().strip('"').strip("'") if m else None


def get_field_description(fm):
    """Extract description value, resolving block scalars (>-, |, ...)."""
    lines = fm.split('\n')
    for i, l in enumerate(lines):
        m = re.match(r'^description:\s*(.*)$', l)
        if not m:
            continue
        head = m.group(1).strip()
        if head in ('>-', '>', '>+', '|', '|-', '|+'):
            folded = head.startswith('>')
            block = []
            for j in range(i + 1, len(lines)):
                # block ends at first non-indented non-empty line (next key)
                if lines[j].strip() != '' and re.match(r'^\S', lines[j]):
                    break
                block.append(lines[j])
            text = '\n'.join(b.strip() for b in block).strip()
            if folded:
                text = re.sub(r'\n+', ' ', text)
            return text
        return head.strip().strip('"').strip("'")
    return None


def has_trigger_clause(desc):
    if not desc:
        return False
    if re.search(r'\bTrigger', desc):
        return True
    # at least two quoted phrases counts as a trigger list
    return len(re.findall(r'"[^"]+"', desc)) >= 2


def check_ref_links(body, skill_dir):
    """Find relative references/*.md mentions and verify they exist."""
    broken = []
    # markdown links ](references/x.md) and bare references/x.md tokens
    cands = set(re.findall(r'\(?(references/[^\s`)\]"\']+\.md)', body))
    for rel in cands:
        # Platzhalter in Prosa (references/<filename>.md) sind keine echten Links
        if '<' in rel or '>' in rel:
            continue
        if not os.path.isfile(os.path.join(skill_dir, rel)):
            broken.append(rel)
    return sorted(broken)


def lint_file(path, is_command=False):
    """Return list of (severity, message)."""
    issues = []
    try:
        txt = open(path, encoding='utf-8').read()
    except Exception as e:
        return [('ERROR', f'unreadable: {e}')]
    fm, body = split_frontmatter(txt)
    if fm is None:
        return [('ERROR', 'kein YAML-Frontmatter')]
    skill_dir = os.path.dirname(path)
    dirname = os.path.basename(skill_dir)

    name = get_field_name(fm)
    if name is None:
        issues.append(('ERROR', 'name fehlt'))
    else:
        if any(r in name.lower() for r in RESERVED):
            issues.append(('ERROR', f'name enthaelt Reserved-Word: {name}'))
        if not NAME_RE.match(name):
            issues.append(('WARN', f'name verletzt ^[a-z0-9-]{{1,64}}$ (Unterstrich/Non-ASCII?): {name}'))
        if not is_command and name != dirname:
            issues.append(('WARN', f'name ({name}) != Verzeichnis ({dirname})'))

    desc = get_field_description(fm)
    if not desc:
        issues.append(('ERROR', 'description fehlt oder leer'))
    else:
        dl = len(desc)
        if dl > DESC_HARD:
            issues.append(('ERROR', f'description {dl} > {DESC_HARD} (Hard-Truncation, Trigger fallen weg)'))
        elif dl > DESC_CAP:
            issues.append(('WARN', f'description {dl} > {DESC_CAP} (ueber Cap)'))
        if not is_command and not has_trigger_clause(desc):
            issues.append(('WARN', 'keine Trigger-Klausel in description'))

    body_lines = body.count('\n') + 1
    if body_lines > BODY_MAX:
        issues.append(('WARN', f'body {body_lines} Zeilen > {BODY_MAX} (Progressive Disclosure noetig)'))

    for rel in check_ref_links(body, skill_dir):
        issues.append(('ERROR', f'kaputter Referenz-Link: {rel}'))

    return issues


def collect_targets(skills_dir, commands_dir, do_commands):
    targets = []
    if os.path.isdir(skills_dir):
        for name in sorted(os.listdir(skills_dir)):
            if name.startswith('_'):
                continue
            p = os.path.join(skills_dir, name, 'SKILL.md')
            if os.path.isfile(p):
                targets.append((p, False))
    if do_commands and os.path.isdir(commands_dir):
        for name in sorted(os.listdir(commands_dir)):
            if name.endswith('.md'):
                targets.append((os.path.join(commands_dir, name), True))
    return targets


def main():
    ap = argparse.ArgumentParser(description='Skill-Autoren-Linter')
    ap.add_argument('--skills-dir', default=DEFAULT_SKILLS)
    ap.add_argument('--commands-dir', default=DEFAULT_COMMANDS)
    ap.add_argument('--commands', action='store_true', help='commands/ mitpruefen')
    ap.add_argument('--quiet', action='store_true', help='nur Verstoesse')
    ap.add_argument('--files', nargs='*', help='nur diese Dateien pruefen (fuer Pre-Commit)')
    args = ap.parse_args()

    if args.files:
        targets = []
        for f in args.files:
            if not os.path.isfile(f):
                continue
            if os.sep + '_shared' + os.sep in os.path.abspath(f):
                continue  # geteilte Docs sind keine Skills
            is_cmd = os.sep + 'commands' + os.sep in os.path.abspath(f)
            targets.append((f, is_cmd))
    else:
        targets = collect_targets(args.skills_dir, args.commands_dir, args.commands)
    n_err = n_warn = n_clean = 0
    for path, is_cmd in targets:
        issues = lint_file(path, is_cmd)
        label = os.path.relpath(path, os.path.dirname(args.skills_dir))
        errs = [i for i in issues if i[0] == 'ERROR']
        warns = [i for i in issues if i[0] == 'WARN']
        n_err += len(errs)
        n_warn += len(warns)
        if not issues:
            n_clean += 1
            if not args.quiet:
                print(f'  ok   {label}')
            continue
        print(f'  {"ERR " if errs else "warn"} {label}')
        for sev, msg in issues:
            print(f'         [{sev}] {msg}')
    print('-' * 60)
    print(f'Skills geprueft: {len(targets)} | sauber: {n_clean} | '
          f'ERROR: {n_err} | WARN: {n_warn}')
    return 1 if n_err else 0


if __name__ == '__main__':
    sys.exit(main())
