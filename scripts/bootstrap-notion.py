#!/usr/bin/env python3
"""Bootstrap Notion schema for Chief of Staff.

Creates a "Chief of Staff" container page under each teamspace home, then
four databases inside it with proper cross-relations:

  Projects      ← (dual) — Stakeholders.Projects
                ← (dual) — Decisions.Projects
                ← (dual) — Tasks.Project
  Tasks.Parent Task — (single) → Tasks   (self-relation for hierarchy)

Usage:
  NOTION_TOKEN=ntn_xxx python3 scripts/bootstrap-notion.py

Idempotent: if a "Chief of Staff" page already exists under a teamspace home,
that teamspace is skipped (rerun after deleting it to recreate from scratch).

Writes the resulting ID map to .claude/notion-workspace-map.json (gitignored).
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

# Teamspace home page IDs discovered via /v1/search after user renamed them.
TEAMSPACES = {
    "personal":   "ef007c17-0e5b-832f-991f-01fb05640c75",
    "3cv":        "32e07c17-0e5b-823a-b8e3-017ee9f4eb52",
    "grantdrive": "7ea07c17-0e5b-8312-aa2e-8105251fe4af",
}


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


def find_child_page(parent_page_id: str, title: str) -> str | None:
    """Return the page_id of a child page with the given title, or None."""
    res = api("GET", f"/blocks/{parent_page_id}/children?page_size=100")
    for b in res.get("results", []):
        if b.get("type") == "child_page" and b["child_page"]["title"] == title:
            return b["id"]
    return None


def create_page(parent_page_id: str, title: str) -> dict:
    return api("POST", "/pages", {
        "parent": {"page_id": parent_page_id},
        "properties": {"title": {"title": [{"text": {"content": title}}]}},
    })


def create_db(parent_page_id: str, title: str, properties: dict) -> dict:
    return api("POST", "/databases", {
        "parent": {"type": "page_id", "page_id": parent_page_id},
        "title": [{"text": {"content": title}}],
        "properties": properties,
    })


def update_db(db_id: str, properties: dict) -> dict:
    return api("PATCH", f"/databases/{db_id}", {"properties": properties})


def relation_dual(target_db_id: str) -> dict:
    # Dual property auto-creates the reciprocal column on target db.
    return {"relation": {
        "database_id": target_db_id,
        "type": "dual_property",
        "dual_property": {},
    }}


def relation_single(target_db_id: str) -> dict:
    return {"relation": {
        "database_id": target_db_id,
        "type": "single_property",
        "single_property": {},
    }}


STATUS_OPTIONS = [
    {"name": "Not Started", "color": "gray"},
    {"name": "In Progress", "color": "blue"},
    {"name": "Blocked",     "color": "red"},
    {"name": "Done",        "color": "green"},
]
PRIORITY_OPTIONS = [
    {"name": "P0", "color": "red"},
    {"name": "P1", "color": "orange"},
    {"name": "P2", "color": "yellow"},
    {"name": "P3", "color": "gray"},
]
HIGH_MED_LOW = [
    {"name": "High",   "color": "red"},
    {"name": "Medium", "color": "yellow"},
    {"name": "Low",    "color": "gray"},
]
DECISION_STATUS = [
    {"name": "Proposed",   "color": "gray"},
    {"name": "Decided",    "color": "green"},
    {"name": "Revisited",  "color": "yellow"},
    {"name": "Superseded", "color": "red"},
]


def bootstrap(context: str, home_id: str) -> dict:
    print(f"\n=== {context.upper()} (home={home_id}) ===")

    existing = find_child_page(home_id, "Chief of Staff")
    if existing:
        print(f"  Chief of Staff page already exists: {existing} — skipping.")
        return {"cos_page": existing, "skipped": True}

    cos = create_page(home_id, "Chief of Staff")
    cos_id = cos["id"]
    print(f"  Created Chief of Staff page: {cos_id}")

    projects = create_db(cos_id, "Projects", {
        "Name":     {"title": {}},
        "Status":   {"select": {"options": STATUS_OPTIONS}},
        "Owner":    {"rich_text": {}},
        "DueDate":  {"date": {}},
        "Priority": {"select": {"options": PRIORITY_OPTIONS}},
        "Notes":    {"rich_text": {}},
    })
    projects_id = projects["id"]
    print(f"  Projects DB:     {projects_id}")

    stakeholders = create_db(cos_id, "Stakeholders", {
        "Name":      {"title": {}},
        "Role":      {"rich_text": {}},
        "Influence": {"select": {"options": HIGH_MED_LOW}},
        "Interest":  {"select": {"options": HIGH_MED_LOW}},
        "Projects":  relation_dual(projects_id),
    })
    stakeholders_id = stakeholders["id"]
    print(f"  Stakeholders DB: {stakeholders_id}")

    decisions = create_db(cos_id, "Decisions", {
        "ID":        {"title": {}},
        "Status":    {"select": {"options": DECISION_STATUS}},
        "Decider":   {"rich_text": {}},
        "Date":      {"date": {}},
        "Rationale": {"rich_text": {}},
        "Projects":  relation_dual(projects_id),
    })
    decisions_id = decisions["id"]
    print(f"  Decisions DB:    {decisions_id}")

    tasks = create_db(cos_id, "Tasks", {
        "Name":     {"title": {}},
        "Status":   {"select": {"options": STATUS_OPTIONS}},
        "DueDate":  {"date": {}},
        "Priority": {"select": {"options": PRIORITY_OPTIONS}},
        "Project":  relation_dual(projects_id),
    })
    tasks_id = tasks["id"]
    print(f"  Tasks DB:        {tasks_id}")

    update_db(tasks_id, {"Parent Task": relation_single(tasks_id)})
    print("  Added self-relation 'Parent Task' on Tasks DB")

    # Notion auto-names the reciprocal of each dual relation "Related to X (Y)".
    # Rename them to clean names on the Projects side.
    update_db(projects_id, {
        "Related to Stakeholders (Projects)": {"name": "Stakeholders"},
        "Related to Decisions (Projects)":    {"name": "Decisions"},
        "Related to Tasks (Project)":         {"name": "Tasks"},
    })
    print("  Renamed reciprocal columns on Projects DB")

    return {
        "cos_page":     cos_id,
        "projects":     projects_id,
        "tasks":        tasks_id,
        "decisions":    decisions_id,
        "stakeholders": stakeholders_id,
    }


def main() -> None:
    out: dict[str, dict] = {}
    for name, page_id in TEAMSPACES.items():
        out[name] = bootstrap(name, page_id)

    map_path = Path(".claude/notion-workspace-map.json")
    map_path.parent.mkdir(parents=True, exist_ok=True)
    map_path.write_text(json.dumps(out, indent=2) + "\n")
    print(f"\nWrote {map_path}")


if __name__ == "__main__":
    main()
