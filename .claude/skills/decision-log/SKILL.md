---
name: decision-log
description: Track decisions made, rationale, alternatives considered, and who approved. Maintains institutional memory and enables decision audits.
allowed-tools: Read Grep Glob Bash Write Edit TodoWrite
argument-hint: [decision to log, topic to review, or "show recent decisions"]
---

# Decision Log — Institutional Memory

You maintain a structured decision log that preserves the **why** behind decisions, not just the **what**. This is critical institutional memory that prevents re-litigating settled issues and helps onboard new stakeholders.

## Decision Log File — Context-Aware

Data is namespaced by context. Read the current context first:

```bash
CONTEXT=$(./scripts/context-path.sh)   # personal | 3cv | grantdrive
LOG=".claude/contexts/$CONTEXT/decisions.md"
```

- **When writing:** Always write to `.claude/contexts/[current-context]/decisions.md`.
- **When reading (personal master only):** Read from all three contexts
  (`.claude/contexts/*/decisions.md`) and label each entry with its source
  context (e.g., `[3cv] DEC-42`). This gives a unified view.
- **When reading (work instances):** Only read from your own context's file.

Each entry follows this format:

### Entry Format

```markdown
## [YYYY-MM-DD] Decision Title

**ID:** DEC-[sequential number]
**Status:** Decided | Pending | Revisit by [date] | Reversed (see DEC-XXX)
**Decider:** [Who made the final call]
**Stakeholders consulted:** [Who was involved]

**Context:** [What situation prompted this decision? 2-3 sentences max.]

**Decision:** [What was decided? Be precise and unambiguous.]

**Alternatives Considered:**
1. **[Option A]** — [Pros]. Rejected because [reason].
2. **[Option B]** — [Pros]. Rejected because [reason].

**Rationale:** [Why this option won. What were the deciding factors?]

**Consequences / Trade-offs:** [What are we accepting by choosing this?]

**Review trigger:** [When should this be revisited? e.g., "If revenue exceeds $X", "After Q3", "Never — permanent"]

---
```

## Modes

### Mode 1: Log a New Decision
When the user describes a decision made:
1. Extract the key elements (context, options, rationale)
2. Assign the next sequential DEC-ID (scoped within the current context)
3. Write the entry to `.claude/contexts/[current-context]/decisions.md`
4. Confirm what was logged (include the context: "Logged to [3cv] as DEC-42")

### Mode 2: Review Decision History
When asked to show decisions:
- **Recent:** Show last 5-10 decisions with ID, date, title, status
- **By topic:** Search the log for related decisions using Grep
- **Pending:** Show all decisions with status "Pending"
- **Due for review:** Show decisions whose review trigger may apply

### Mode 3: Decision Support
When asked to help make a new decision:

#### Decision Brief: [Topic]

**Context:** [Situation summary]

| Option | Pros | Cons | Risk | Reversibility | Effort |
|--------|------|------|------|---------------|--------|
| A: ... | ... | ... | H/M/L | Easy/Hard | H/M/L |
| B: ... | ... | ... | H/M/L | Easy/Hard | H/M/L |
| C: Status quo | ... | ... | H/M/L | N/A | None |

**Recommendation:** [Option] because [one-sentence rationale].

**Related past decisions:** [Search log for relevant precedents]

After the user decides, automatically log it (Mode 1).

### Mode 4: Decision Audit
Generate a summary report:
- Total decisions logged
- Decisions by status (Decided / Pending / Reversed)
- Decisions due for review
- Decisions reversed (and why — pattern analysis)
- Areas with no documented decisions (governance gaps)

## Principles

1. **Decisions without rationale are useless.** Always capture the "why."
2. **Capture what was rejected too.** This prevents revisiting the same dead ends.
3. **Set review triggers.** Decisions aren't permanent unless explicitly marked so.
4. **Link related decisions.** Reference DEC-IDs to build a decision graph.

## Input

$ARGUMENTS
