#!/usr/bin/env bash
# sync-contexts.sh — Pull work context data into the personal master branch
#
# Run this ONLY on the personal master instance. It fetches each work context
# branch and merges its .claude/contexts/[context]/ tree into the current
# branch (typically main), producing a unified view.
#
# The work instances NEVER run this — they only push to their own branches.
#
# Usage:   ./scripts/sync-contexts.sh

set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT"

CURRENT_BRANCH="$(git rev-parse --abbrev-ref HEAD)"

# Safety: only sync when on the master branch
if [[ "$CURRENT_BRANCH" != "main" && "$CURRENT_BRANCH" != "master" ]]; then
  echo "Refusing to sync: not on main/master (current: $CURRENT_BRANCH)"
  echo "Sync should only run on the personal master branch."
  exit 1
fi

# Safety: refuse if there are uncommitted changes
if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "Refusing to sync: uncommitted changes in working tree."
  echo "Commit or stash first."
  exit 1
fi

WORK_CONTEXTS=(3cv grantdrive)

echo "Fetching all branches..."
git fetch --all --prune

changes_made=false

for ctx in "${WORK_CONTEXTS[@]}"; do
  branch="context/$ctx"
  ctx_path=".claude/contexts/$ctx"

  if ! git show-ref --verify --quiet "refs/remotes/origin/$branch"; then
    echo "  [$ctx] Remote branch 'origin/$branch' not found — skipping."
    continue
  fi

  echo "  [$ctx] Syncing from origin/$branch..."

  # Grab just the contexts/[ctx]/ subtree from that branch
  # Using `git checkout origin/<branch> -- <path>` stages the files
  if git checkout "origin/$branch" -- "$ctx_path" 2>/dev/null; then
    if ! git diff --cached --quiet -- "$ctx_path"; then
      changes_made=true
      echo "    → updates staged for $ctx_path"
    else
      echo "    → no changes for $ctx_path"
      git reset HEAD -- "$ctx_path" >/dev/null 2>&1 || true
    fi
  else
    echo "    → $ctx_path not present on origin/$branch — skipping."
  fi
done

if [[ "$changes_made" == "true" ]]; then
  echo ""
  echo "Committing sync..."
  git commit -m "Sync work context data from remote branches

Pulled latest .claude/contexts/{3cv,grantdrive}/ from their respective
context branches into the personal master view."
  echo ""
  echo "Done. Run 'git push' to publish the updated master view."
else
  echo ""
  echo "No changes to sync."
fi
