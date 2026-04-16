#!/usr/bin/env bash
# Apply environment-specific patches to workspace-mcp (Google Workspace MCP).
#
# Two issues we hit in this sandbox environment:
#   1. The OAuth userinfo call uses googleapiclient `build("oauth2", "v2")`,
#      which fails silently (discovery 404). Fix: replace get_user_info() with
#      a direct HTTP call to /oauth2/v2/userinfo.
#   2. httplib2 (used by googleapiclient) has its own bundled CA cert file
#      that doesn't trust the sandbox's TLS-intercepting proxy. Fix: copy the
#      system CA bundle over httplib2's and certifi's bundles.
#
# Rerun after workspace-mcp reinstalls or uv cache wipes. Idempotent.
set -euo pipefail

SYSBUNDLE=/etc/ssl/certs/ca-certificates.crt
[ -r "$SYSBUNDLE" ] || { echo "missing $SYSBUNDLE"; exit 1; }

# Find all installed workspace-mcp copies (uv caches per-version).
mapfile -t pkg_roots < <(
  find /root/.cache/uv/archive-v0 -maxdepth 6 -type d -name 'workspace_mcp-*.dist-info' 2>/dev/null \
    | sed 's|/workspace_mcp-[^/]*\.dist-info$||' | sort -u
)

if [ "${#pkg_roots[@]}" -eq 0 ]; then
  echo "No workspace-mcp install found under /root/.cache/uv"
  exit 1
fi

for root in "${pkg_roots[@]}"; do
  echo "Patching workspace-mcp install at $root"

  # --- Fix 1: overwrite httplib2 & certifi CA bundles ---
  for bundle in "$root/httplib2/cacerts.txt" "$root/certifi/cacert.pem"; do
    if [ -f "$bundle" ]; then
      cp "$SYSBUNDLE" "$bundle"
      echo "  ca bundle -> $bundle"
    fi
  done

  # --- Fix 2: patch auth/google_auth.py:get_user_info to use direct HTTP ---
  auth_file="$root/auth/google_auth.py"
  if [ -f "$auth_file" ] && ! grep -q 'PATCHED_USERINFO_DIRECT_HTTP' "$auth_file"; then
    python3 - "$auth_file" <<'PY'
import sys, re
p = sys.argv[1]
s = open(p).read()
old = '''def get_user_info(
    credentials: Credentials, *, skip_valid_check: bool = False
) -> Optional[Dict[str, Any]]:
    """Fetches basic user profile information (requires userinfo.email scope)."""
    if not credentials:
        logger.error("Cannot get user info: Missing credentials.")
        return None
    if not skip_valid_check and not credentials.valid:
        logger.error("Cannot get user info: Invalid credentials.")
        return None
    service = None
    try:
        # Using googleapiclient discovery to get user info
        # Requires 'google-api-python-client' library
        service = build("oauth2", "v2", credentials=credentials)
        user_info = service.userinfo().get().execute()
        logger.info(f"Successfully fetched user info: {user_info.get('email')}")
        return user_info
    except HttpError as e:
        logger.error(f"HttpError fetching user info: {e.status_code} {e.reason}")
        # Handle specific errors, e.g., 401 Unauthorized might mean token issue
        return None
    except Exception as e:
        logger.error(f"Unexpected error fetching user info: {e}")
        return None
    finally:
        if service:
            service.close()'''
new = '''def get_user_info(
    credentials: Credentials, *, skip_valid_check: bool = False
) -> Optional[Dict[str, Any]]:
    """Fetches basic user profile information (requires userinfo.email scope).

    PATCHED_USERINFO_DIRECT_HTTP: bypass googleapiclient's build("oauth2","v2"),
    which fails in some environments with a discovery 404. Direct HTTP works.
    """
    if not credentials:
        logger.error("Cannot get user info: Missing credentials.")
        return None
    if not skip_valid_check and not credentials.valid:
        logger.error("Cannot get user info: Invalid credentials.")
        return None
    try:
        import requests as _rq
        r = _rq.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {credentials.token}"},
            timeout=10,
        )
        if r.status_code == 200:
            info = r.json()
            logger.info(f"Successfully fetched user info: {info.get('email')}")
            return info
        logger.error(f"userinfo HTTP {r.status_code}: {r.text[:300]}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error fetching user info: {e}")
        return None'''
if old not in s:
    print(f"WARNING: expected get_user_info block not found verbatim in {p}; skipping patch")
    sys.exit(0)
open(p, 'w').write(s.replace(old, new))
print(f"  patched get_user_info in {p}")
PY
  elif [ -f "$auth_file" ]; then
    echo "  get_user_info already patched"
  fi
done

echo "Done. Restart workspace-mcp (kill the python workspace-mcp PID) to pick up code changes."
