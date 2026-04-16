#!/usr/bin/env bash
# context-path.sh — Helper that outputs the current context's data path.
#
# Usage:
#   ./scripts/context-path.sh                # Prints current context name
#   ./scripts/context-path.sh --dir          # Prints .claude/contexts/[current]
#   ./scripts/context-path.sh --dir foo.md   # Prints .claude/contexts/[current]/foo.md
#   ./scripts/context-path.sh --all          # Prints all context names (newline-delimited)
#   ./scripts/context-path.sh --all-dirs     # Prints all context dirs

set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
MARKER="$REPO_ROOT/.claude/current-context"

current="personal"
if [[ -f "$MARKER" ]]; then
  current="$(tr -d '[:space:]' < "$MARKER")"
  if [[ -z "$current" ]]; then current="personal"; fi
fi

CONTEXTS=(personal 3cv grantdrive)

case "${1:-}" in
  --dir)
    if [[ -n "${2:-}" ]]; then
      echo "$REPO_ROOT/.claude/contexts/$current/$2"
    else
      echo "$REPO_ROOT/.claude/contexts/$current"
    fi
    ;;
  --all)
    for c in "${CONTEXTS[@]}"; do echo "$c"; done
    ;;
  --all-dirs)
    for c in "${CONTEXTS[@]}"; do echo "$REPO_ROOT/.claude/contexts/$c"; done
    ;;
  "")
    echo "$current"
    ;;
  *)
    echo "Usage: $0 [--dir [file]|--all|--all-dirs]" >&2
    exit 2
    ;;
esac
