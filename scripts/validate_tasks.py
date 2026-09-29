#!/usr/bin/env python3
"""Dependency-free Markdown task record checks. Does not prove semantic correctness."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
TASK_RE = re.compile(r'^- \[([ x])\] ([A-Z][A-Z0-9-]*-\d{3,}): (.+)$', re.M)
FIELDS = ('Status', 'Acceptance', 'Dependencies', 'Planned areas', 'Implementation', 'Tests', 'Verification', 'Revision', 'Architecture', 'Documentation', 'Outstanding')
REF_RE = re.compile(r'`([^`\n]+\.[A-Za-z0-9_+-]+):(\d+)-(\d+)`')
VALID = {'Pending', 'In progress', 'Implemented', 'Verified', 'Blocked', 'Completed'}

def validate(path):
    errors = []
    try:
        body = path.read_text(encoding='utf-8')
    except OSError as e:
        return [f'{path}: {e}']
    if not body.startswith('# Feature:'):
        errors.append(f'{path}: missing feature title')
    if 'Scope authorization:' not in body:
        errors.append(f'{path}: missing scope authorization')
    matches = list(TASK_RE.finditer(body))
    if not matches:
        errors.append(f'{path}: no checkbox tasks with stable IDs')
    seen = set()
    for idx, match in enumerate(matches):
        checkbox, task_id, _ = match.groups()
        block = body[match.end():matches[idx + 1].start() if idx + 1 < len(matches) else len(body)]
        if task_id in seen:
            errors.append(f'{path}: duplicate task ID {task_id}')
        seen.add(task_id)
        values = {}
        for field in FIELDS:
            found = re.search(r'^  - ' + re.escape(field) + r':\s*(.*)$', block, re.M)
            if not found:
                errors.append(f'{path}: {task_id} missing {field}')
            else:
                values[field] = found.group(1).strip()
        status = values.get('Status', '')
        if status and status not in VALID:
            errors.append(f'{path}: {task_id} invalid status {status!r}')
        if checkbox == 'x' and status != 'Completed':
            errors.append(f'{path}: {task_id} checked but not Completed')
        if status == 'Completed' and checkbox != 'x':
            errors.append(f'{path}: {task_id} Completed but not checked')
        if status == 'Completed':
            for field in ('Implementation', 'Tests', 'Verification', 'Architecture', 'Documentation'):
                if values.get(field, '').lower() in ('', 'pending'):
                    errors.append(f'{path}: {task_id} completed with pending {field}')
            if not re.search(r'\bPASSED\b', values.get('Verification', '')):
                errors.append(f'{path}: {task_id} completed without PASSED verification')
        if status in ('Implemented', 'Verified', 'Completed') and values.get('Implementation', '').lower() in ('', 'pending'):
            errors.append(f'{path}: {task_id} implemented without implementation references')
        for rel, start, end in REF_RE.findall(block):
            file = ROOT / rel
            if Path(rel).is_absolute() or '..' in Path(rel).parts or not file.is_file():
                errors.append(f'{path}: {task_id} missing or unsafe reference {rel}')
                continue
            count = len(file.read_text(encoding='utf-8', errors='replace').splitlines())
            if not (1 <= int(start) <= int(end) <= count):
                errors.append(f'{path}: {task_id} invalid range {rel}:{start}-{end} (file has {count} lines)')
    return errors

def main():
    if len(sys.argv) > 1:
        paths = [Path(p).resolve() for p in sys.argv[1:]]
    else:
        paths = sorted((ROOT / 'tasks/active').glob('*.md')) + sorted((ROOT / 'tasks/completed').glob('*.md'))
    errors = [e for path in paths for e in validate(path)]
    for error in errors:
        print('ERROR:', error, file=sys.stderr)
    if errors:
        return 1
    print(f'PASS: validated {len(paths)} feature record(s); syntax, task status, and reference bounds only.')
    print('NOTE: No semantic correctness, application tests, or approval enforcement was verified.')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
