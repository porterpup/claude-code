#!/usr/bin/env python3
"""Rebuild .claude/notion-workspace-map.json from live Notion state.

Use when you've bootstrapped on another machine and don't have the map file
locally. Walks each teamspace home → finds the "Chief of Staff" child page →
lists its child databases by title → writes the IDs to the map.

Usage:
  NOTION_TOKEN=ntn_xxx python3 scripts/discover-notion-map.py

Teamspace home IDs are hardcoded (same as bootstrap-notion.py).
"""
from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

TOKEN = os.environ.get("NOTION_TOKEN")
if not TOKEN:
    print("ERROR: NOTION_TOKEN env var required", file=sys.stderr)
    sys.exit(1)

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}

TEAMSPACES = {
    "personal":   "ef007c17-0e5b-832f-991f-01fb05640c75",
    "3cv":        "32e07c17-0e5b-823a-b8e3-017ee9f4eb52",
    "grantdrive": "7ea07c17-0e5b-8312-aa2e-8105251fe4af",
}

DB_TITLE_TO_KEY = {
    "Projects":     "projects",
    "Tasks":        "tasks",
    "Decisions":    "decisions",
    "Stakeholders": "stakeholders",
    "Briefings":    "briefings",
}


def api(method: str, path: str, body: dict | None = None) -> dict:
    data = json.dumps(body).encode() if body is not None else None
    last_err: Exception | None = None
    for attempt in range(4):
        req = urllib.request.Request(
            f"https://api.notion.com/v1{path}",
            method=method,
            headers=HEADERS,
            data=data,
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            if e.code in (502, 503, 504) and attempt < 3:
                time.sleep(2 ** attempt)
                last_err = e
                continue
            raise
        except urllib.error.URLError as e:
            if attempt < 3:
                time.sleep(2 ** attempt)
                last_err = e
                continue
            raise
    assert last_err
    raise last_err


def find_child_page(parent_id: str, title: str) -> str | None:
    res = api("GET", f"/blocks/{parent_id}/children?page_size=100")
    for b in res.get("results", []):
        if b.get("type") == "child_page" and b["child_page"]["title"] == title:
            return b["id"]
    return None


def list_child_dbs(parent_id: str) -> dict[str, str]:
    res = api("GET", f"/blocks/{parent_id}/children?page_size=100")
    found: dict[str, str] = {}
    for b in res.get("results", []):
        if b.get("type") == "child_database":
            title = b["child_database"]["title"]
            key = DB_TITLE_TO_KEY.get(title)
            if key:
                found[key] = b["id"]
    return found


def main() -> None:
    out: dict[str, dict] = {}
    for name, home_id in TEAMSPACES.items():
        print(f"\n=== {name.upper()} (home={home_id}) ===")
        cos_id = find_child_page(home_id, "Chief of Staff")
        if not cos_id:
            print(f"  no 'Chief of Staff' child page found — skipping")
            continue
        print(f"  cos_page: {cos_id}")
        dbs = list_child_dbs(cos_id)
        for key, db_id in dbs.items():
            print(f"  {key}: {db_id}")
        out[name] = {"cos_page": cos_id, **dbs}

    map_path = Path(".claude/notion-workspace-map.json")
    map_path.parent.mkdir(parents=True, exist_ok=True)
    map_path.write_text(json.dumps(out, indent=2) + "\n")
    print(f"\nWrote {map_path}")


if __name__ == "__main__":
    main()
