#!/usr/bin/env bash
# switch-context.sh — Switch between Chief of Staff contexts
#
# Usage:   ./scripts/switch-context.sh [personal|3cv|grantdrive]
#
# This:
#   1. Updates .claude/current-context with the new context name
#   2. Copies .mcp.[context].json → .mcp.json (active MCP config)
#   3. Echoes confirmation

set -euo pipefail

CONTEXT="${1:-}"
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

VALID_CONTEXTS=(personal 3cv grantdrive)

if [[ -z "$CONTEXT" ]]; then
  current="$(cat "$REPO_ROOT/.claude/current-context" 2>/dev/null | tr -d '[:space:]' || echo unknown)"
  echo "Current context: $current"
  echo ""
  echo "Usage: $0 [${VALID_CONTEXTS[*]}]"
  exit 0
fi

# Validate
valid=false
for c in "${VALID_CONTEXTS[@]}"; do
  if [[ "$c" == "$CONTEXT" ]]; then
    valid=true
    break
  fi
done

if [[ "$valid" != "true" ]]; then
  echo "Error: Unknown context '$CONTEXT'"
  echo "Valid contexts: ${VALID_CONTEXTS[*]}"
  exit 1
fi

# Check the MCP template exists
MCP_TEMPLATE="$REPO_ROOT/.mcp.${CONTEXT}.json"
if [[ ! -f "$MCP_TEMPLATE" ]]; then
  echo "Error: MCP template not found: $MCP_TEMPLATE"
  exit 1
fi

# Ensure context dir exists
mkdir -p "$REPO_ROOT/.claude/contexts/$CONTEXT"

# Copy MCP config
cp "$MCP_TEMPLATE" "$REPO_ROOT/.mcp.json"

# Update marker
echo "$CONTEXT" > "$REPO_ROOT/.claude/current-context"

echo "Switched to context: $CONTEXT"
echo "  - .mcp.json         ← .mcp.${CONTEXT}.json"
echo "  - current-context   ← $CONTEXT"
echo "  - data namespace:   .claude/contexts/${CONTEXT}/"
echo ""
echo "Restart Claude Code for the MCP config change to take effect."
