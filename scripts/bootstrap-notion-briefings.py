#!/usr/bin/env python3
"""Add a Briefings database to each teamspace's Chief of Staff page.

Briefings are the I/O substrate between specialist subagents (cos-inbox,
cos-calendar, ...) and the orchestrator. Specialists write structured
findings here; the orchestrator queries by Source/Type/Status/Window.

Idempotent: if a "Briefings" DB already exists under a teamspace's CoS page,
that teamspace is skipped.

Usage:
  NOTION_TOKEN=ntn_xxx python3 scripts/bootstrap-notion-briefings.py

Reads .claude/notion-workspace-map.json for the cos_page / projects / tasks
IDs created by bootstrap-notion.py. Writes the new briefings ID back into
the same file under each teamspace.
"""
from __future__ import annotations

import json
import os
import sys
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

MAP_PATH = Path(".claude/notion-workspace-map.json")
if not MAP_PATH.exists():
    print(f"ERROR: {MAP_PATH} not found. Run bootstrap-notion.py first.", file=sys.stderr)
    sys.exit(1)


def api(method: str, path: str, body: dict | None = None) -> dict:
    data = json.dumps(body).encode() if body is not None else None
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
        body_txt = e.read().decode("utf-8", errors="replace")
        print(f"HTTP {e.code} on {method} {path}: {body_txt}", file=sys.stderr)
        raise


def find_child_db(parent_page_id: str, title: str) -> str | None:
    res = api("GET", f"/blocks/{parent_page_id}/children?page_size=100")
    for b in res.get("results", []):
        if b.get("type") == "child_database" and b["child_database"]["title"] == title:
            return b["id"]
    return None


def create_db(parent_page_id: str, title: str, properties: dict) -> dict:
    return api("POST", "/databases", {
        "parent": {"type": "page_id", "page_id": parent_page_id},
        "title": [{"text": {"content": title}}],
        "properties": properties,
    })


SOURCE_OPTIONS = [
    {"name": "cos-inbox",    "color": "purple"},
    {"name": "cos-calendar", "color": "blue"},
    {"name": "manual",       "color": "gray"},
]
TYPE_OPTIONS = [
    {"name": "triage",          "color": "orange"},
    {"name": "preview",         "color": "yellow"},
    {"name": "task-proposal",   "color": "green"},
    {"name": "draft-proposal",  "color": "green"},
    {"name": "cleanup",         "color": "brown"},
    {"name": "meeting-prep",    "color": "blue"},
    {"name": "schedule-audit",  "color": "blue"},
    {"name": "find-time",       "color": "blue"},
    {"name": "daily-digest",    "color": "pink"},
    {"name": "weekly-summary",  "color": "pink"},
]
STATUS_OPTIONS = [
    {"name": "fresh",    "color": "green"},
    {"name": "consumed", "color": "gray"},
    {"name": "stale",    "color": "red"},
]


def bootstrap_briefings(context: str, ids: dict) -> str | None:
    print(f"\n=== {context.upper()} ===")
    cos_page = ids.get("cos_page")
    if not cos_page:
        print(f"  no cos_page in map for {context} — skipping")
        return None

    existing = find_child_db(cos_page, "Briefings")
    if existing:
        print(f"  Briefings DB already exists: {existing} — skipping")
        return existing

    properties = {
        "Name":   {"title": {}},
        "Source": {"select": {"options": SOURCE_OPTIONS}},
        "Type":   {"select": {"options": TYPE_OPTIONS}},
        "Window": {"rich_text": {}},
        "Status": {"select": {"options": STATUS_OPTIONS}},
        "Created": {"created_time": {}},
    }
    if ids.get("tasks"):
        properties["Related Tasks"] = {"relation": {
            "database_id": ids["tasks"],
            "type": "single_property",
            "single_property": {},
        }}
    if ids.get("projects"):
        properties["Related Projects"] = {"relation": {
            "database_id": ids["projects"],
            "type": "single_property",
            "single_property": {},
        }}

    db = create_db(cos_page, "Briefings", properties)
    print(f"  Created Briefings DB: {db['id']}")
    return db["id"]


def main() -> None:
    workspace_map = json.loads(MAP_PATH.read_text())
    changed = False
    for context, ids in workspace_map.items():
        if not isinstance(ids, dict):
            continue
        briefings_id = bootstrap_briefings(context, ids)
        if briefings_id and ids.get("briefings") != briefings_id:
            ids["briefings"] = briefings_id
            changed = True

    if changed:
        MAP_PATH.write_text(json.dumps(workspace_map, indent=2) + "\n")
        print(f"\nUpdated {MAP_PATH}")
    else:
        print("\nNothing to update.")


if __name__ == "__main__":
    main()
