#!/usr/bin/env bash
# Stop all Slack agent runners.
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
if pkill -f "python3 ${DIR}/runner.py"; then
  echo "Runners stopped."
else
  echo "No runners were running."
fi
