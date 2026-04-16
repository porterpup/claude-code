# Decision Log — personal

---

## [2026-04-14] Adopt multi-context architecture for Chief of Staff

**ID:** DEC-1
**Status:** Decided
**Decider:** You
**Stakeholders consulted:** None (solo decision)

**Context:** Running a single unified Chief of Staff for personal, 3CV (W2 job), and Grant Drive activities risks leaking data across domains. Work tools bill to work accounts; personal tools bill to personal. Need a way to keep contexts isolated at the edges while still producing a single source of truth for "what's on my plate."

**Decision:** Split into three contexts — `personal`, `3cv`, `grantdrive` — each with its own credentials, MCP config, and data namespace under `.claude/contexts/[name]/`. All share the same skills. The personal master aggregates all three for the unified view. Git branches enforce the isolation boundary (work branches don't contain personal data).

**Alternatives Considered:**
1. **Single shared data store** — Simplest. Rejected because it leaks work data to personal tools and vice versa, and blurs billing boundaries.
2. **Three fully separate repos** — Strong isolation. Rejected because skill updates would have to be duplicated three times, and there would be no unified view without heavy cross-repo plumbing.
3. **Environment variable overlay on shared data** — Middle ground. Rejected because the isolation is enforced only by convention, not by the repo structure itself.

**Rationale:** The namespace + branch approach gives us the best of both: skills stay DRY (one repo), personal master gets the unified view, and work instances literally cannot see personal data because it isn't on their branch.

**Consequences / Trade-offs:**
- Adds one bit of process overhead — must pick/switch context before working.
- Personal master has to run `sync-contexts.sh` to pull work data.
- If 3CV doesn't let us take data off their systems, the sync step can't happen on that side — acceptable, we just lose the aggregate view for that context.

**Review trigger:** Revisit if a fourth context is needed, or if a context's data never ends up worth aggregating.

---

## [2026-04-15] Use Notion as the task/project hierarchy tool

**ID:** DEC-2
**Status:** Decided
**Decider:** You
**Stakeholders consulted:** None (solo decision)

**Context:** Needed a task/project tool that (a) supports multi-level work hierarchy (projects → tasks → subtasks), (b) has a generous-enough free tier for three contexts long-term, (c) has a maintained MCP server, and (d) can mirror the markdown-file source of truth bidirectionally. Originally blueprinted as Trello, but Trello has no real hierarchy.

**Decision:** Adopt Notion. One workspace on the personal plan with three teamspaces (Personal, 3CV, GrantDrive) mapped 1:1 to the existing context architecture. A single Internal Integration is shared into each teamspace. Under each teamspace home, a "Chief of Staff" container page holds four databases: Projects, Tasks (with self-relation for parent/child hierarchy), Decisions, Stakeholders — with dual-property relations wiring Projects ↔ everything. Markdown files remain the source of truth for decisions/projects; Notion is the phone-accessible view layer and the place subtasks actually live.

**Alternatives Considered:**
1. **Trello** — No task hierarchy (just cards + checklists). Rejected when hierarchy became a hard requirement.
2. **Linear** — Great hierarchy and MCP support, but free tier caps at 250 issues and 2 teams. Three-context architecture needs at least 3 teams, and 250 issues is a low ceiling for multi-year use.
3. **ClickUp** — Unlimited tasks on free, but free plan caps at 5 spaces and the API/MCP story is less clean.
4. **Asana / Todoist / Monday** — Similar hierarchy stories but no first-party MCP server we trust to stay maintained.
5. **Stay markdown-only, skip the task tool** — Rejected because the phone use case (adding tasks while out, checking status on mobile) is a primary motivator.

**Rationale:** Notion is the only option that clears all four bars: unlimited pages/blocks/databases on free, native block-level hierarchy, official `@notionhq/notion-mcp-server`, and a well-documented REST API we can hit directly when the MCP is offline. The teamspace model happens to map perfectly onto our context boundaries.

**Consequences / Trade-offs:**
- Adds Notion as a runtime dependency — if Notion is down, tasks aren't writable via the tool; markdown fallback still works.
- Bidirectional sync between markdown and Notion is additional code we'll need (deferred to a later phase).
- Relation properties on the Projects DB are auto-named ugly reciprocals ("Related to X (Y)") — bootstrap script handles the rename, but manual renames in Notion will drift from the script.
- Free-tier Notion integrations see only what's explicitly shared with them — if a new teamspace is added later, we must remember to share the integration into it.

**Review trigger:** Revisit if we hit Notion rate limits routinely, if Notion changes its free-tier terms, or if manual token rotation becomes annoying.

---
