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
