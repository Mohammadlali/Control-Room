#!/usr/bin/env python3
"""
check_links.py -- Gate: verify internal file links in markdown docs.

Scans all .md files under the repo root for relative file links
(e.g. [text](./other.md) or [text](Team/MAP.md)) and checks each
target path exists. External http/https links are skipped to avoid
non-deterministic network failures.

Exit 0 = all internal links valid (silent).
Exit 1 = broken links found (prints report).
"""
import os
import re
import sys
import urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Matches markdown links: [text](target)
LINK_RE = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

# Directories to skip entirely
SKIP_DIRS = {'.git', 'node_modules', '.github'}

# External schemes to skip
EXTERNAL_SCHEMES = (
    'http://', 'https://', 'mailto:', 'ftp://', 'tel:',
    'javascript:', 'file://', 'conversation://', 'urn:'
)


def collect_md_files(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fname in filenames:
            if fname.endswith('.md'):
                yield os.path.join(dirpath, fname)


def check_file(md_path):
    broken = []
    in_code_block = False
    with open(md_path, encoding='utf-8', errors='replace') as f:
        for lineno, line in enumerate(f, 1):
            stripped = line.strip()
            if stripped.startswith('```'):
                in_code_block = not in_code_block
                continue
            if in_code_block:
                continue

            for _, target in LINK_RE.findall(line):
                target = target.strip()
                # Handle optional title in link: [text](path "title") or [text](path 'title')
                if ' ' in target:
                    target = target.split(None, 1)[0]
                # Strip anchor fragments
                target = target.split('#')[0].strip()
                # URL-decode path
                target = urllib.parse.unquote(target)

                # Skip external links, anchors-only, empty
                if not target or target.startswith(EXTERNAL_SCHEMES):
                    continue

                # Check path resolution:
                # 1. Relative to repo root if path starts with '/'
                # 2. Relative to current file's directory
                # 3. Fallback: relative to repo root
                if target.startswith('/'):
                    resolved = os.path.normpath(os.path.join(ROOT, target.lstrip('/')))
                else:
                    resolved = os.path.normpath(os.path.join(os.path.dirname(md_path), target))
                    if not os.path.exists(resolved):
                        resolved_root = os.path.normpath(os.path.join(ROOT, target))
                        if os.path.exists(resolved_root):
                            resolved = resolved_root

                if not os.path.exists(resolved):
                    rel_md = os.path.relpath(md_path, ROOT)
                    broken.append(f'  {rel_md}:{lineno} -> {target}')
    return broken


def main():
    all_broken = []
    for md_file in collect_md_files(ROOT):
        all_broken.extend(check_file(md_file))

    if not all_broken:
        sys.exit(0)

    sys.stderr.write('FAIL: Broken internal links found:\n')
    for entry in all_broken:
        sys.stderr.write(entry + '\n')
    sys.exit(1)


if __name__ == '__main__':
    main()
