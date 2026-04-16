#!/usr/bin/env bash
# Start all Slack agent runners in the background.
# Usage: ./start-runners.sh          (start all)
#        ./start-runners.sh cos-inbox (start one)

set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
LOGDIR="/tmp"

AGENTS=("cos" "cos-notion" "cos-inbox")

if [[ ${1:-} ]]; then
  AGENTS=("$1")
fi

# Kill any existing runners first.
pkill -f "python3 ${DIR}/runner.py" 2>/dev/null || true
sleep 1

for agent in "${AGENTS[@]}"; do
  log="${LOGDIR}/slack-${agent}.log"
  AGENT="$agent" nohup python3 "${DIR}/runner.py" >>"$log" 2>&1 &
  echo "${agent} started (pid=$!, log=${log})"
done

sleep 3
for agent in "${AGENTS[@]}"; do
  echo "--- ${agent} ---"
  tail -3 "${LOGDIR}/slack-${agent}.log"
done
