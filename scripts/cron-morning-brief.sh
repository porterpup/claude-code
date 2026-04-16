#!/usr/bin/env bash
# Headless morning brief — runs cos-inbox + cos-calendar specialists,
# writes Briefings to Notion. Designed for cron.
#
# Crontab example (7am Mon-Fri, personal context):
#   0 7 * * 1-5 cd /home/user/claude-code && ./scripts/cron-morning-brief.sh >> /tmp/cos-morning.log 2>&1
#
# Notes:
#   - Runs `claude -p` headless. No interactive UI.
#   - The orchestrator spawns both specialists in parallel via the Agent tool.
#   - Each specialist writes its Briefing to Notion and returns one line.
#   - Output to stdout is the orchestrator's terse roll-up. Real detail lives in Notion.
#   - On failure (network, auth, missing env), exits non-zero so cron mails you.

set -euo pipefail

cd "$(dirname "$0")/.."
REPO_ROOT="$(pwd)"

CONTEXT="${COS_CONTEXT:-personal}"
echo "$CONTEXT" > .claude/current-context

PROMPT="Morning brief for context=${CONTEXT}. Spawn cos-inbox (triage last 24h) and cos-calendar (prep today) in parallel. When both return, do NOT re-summarize their work — just print the two pointer lines they returned, plus a one-sentence top-line ('N items need attention'). Detail lives in Notion."

if ! command -v claude >/dev/null 2>&1; then
  echo "ERROR: claude CLI not on PATH" >&2
  exit 1
fi

claude -p "$PROMPT" \
  --append-system-prompt "You are running headless via cron. No follow-up questions. Be terse. If a specialist errors, surface its error verbatim and exit." \
  --output-format text
