#!/usr/bin/env python3
"""Dependency-free structural validation. Not an application or architecture compliance test."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    'AGENTS.md', 'agent.md', 'architecture/CONTRACT.yaml',
    'tasks/templates/FEATURE.md', 'scripts/validate_tasks.py',
    'docs/engineering/TASK_WORKFLOW.md',
    'architecture/README.md', 'docs/product/PRODUCT.md',
    'docs/engineering/COMMANDS.md', 'docs/engineering/CHANGE_POLICY.md',
    'docs/engineering/COMMUNICATION.md', 'docs/operations/OBSERVABILITY.md',
    '.github/CODEOWNERS', '.github/workflows/governance.yml',
]
errors = []
for name in REQUIRED:
    if not (ROOT / name).is_file():
        errors.append(f'Missing required file: {name}')
for skill in sorted((ROOT / '.agents/skills').glob('*/SKILL.md')):
    body = skill.read_text(encoding='utf-8')
    match = re.match(r'\A---\n(.*?)\n---\n', body, re.S)
    if not match:
        errors.append(f'Missing YAML frontmatter: {skill.relative_to(ROOT)}')
        continue
    front = match.group(1)
    name = re.search(r'^name:\s*(.+)$', front, re.M)
    desc = re.search(r'^description:\s*(.+)$', front, re.M)
    if not name or name.group(1).strip() != skill.parent.name:
        errors.append(f'Invalid skill name: {skill.relative_to(ROOT)}')
    if not desc or not desc.group(1).strip():
        errors.append(f'Missing skill description: {skill.relative_to(ROOT)}')
if not list((ROOT / '.agents/skills').glob('*/SKILL.md')):
    errors.append('No agent skills found')
contract = ROOT / 'architecture/CONTRACT.yaml'
if contract.exists():
    content = contract.read_text(encoding='utf-8')
    for key in ('version:', 'project:', 'status:', 'components:', 'protected_changes:'):
        if not re.search(r'^' + re.escape(key), content, re.M):
            errors.append(f'Architecture contract missing {key}')
    if 'status: uninitialized' in content:
        print('WARNING: Architecture contract is uninitialized; configure before autonomous development.')
commands = ROOT / 'docs/engineering/COMMANDS.md'
if commands.exists() and '[CUSTOMIZE]' in commands.read_text(encoding='utf-8'):
    print('WARNING: Application verification commands are unconfigured.')
if errors:
    for error in errors:
        print(f'ERROR: {error}', file=sys.stderr)
    sys.exit(1)
print('PASS: starter structure, skill frontmatter, and contract keys validated.')
print('NOTE: No application tests, dependency enforcement, security scans, or approval checks were executed.')
