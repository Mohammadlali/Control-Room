#!/usr/bin/env bash
# Tools/install_hooks.sh
# One-time setup: activates the .githooks directory as the git hooks path.
# Works with AGY, Claude, Cursor, or any agent (agent-agnostic).
#
# Usage:
#   bash Tools/install_hooks.sh

set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

git config core.hooksPath .githooks
chmod +x .githooks/pre-commit 2>/dev/null || true

echo "Hooks installed."
echo "The following checks now run before every commit:"
echo "  - check_workflow_safety: validates .github/workflows/*.yml"
echo "    * no double-quotes in printf content strings"
echo "    * no under-indented Python inline in YAML blocks"
echo "    * YAML syntax validity"
echo ""
echo "To bypass once (not recommended): git commit --no-verify"
echo "To uninstall: git config --unset core.hooksPath"
