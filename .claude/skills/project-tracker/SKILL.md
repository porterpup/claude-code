---
name: project-tracker
description: Track multiple projects/initiatives with status, milestones, dependencies, and risks. Persistent dashboard across sessions.
allowed-tools: Read Grep Glob Bash Write Edit TodoWrite
argument-hint: [project name, "add project", "update [project]", or "show dashboard"]
---

# Multi-Project Tracker

You maintain a persistent project portfolio dashboard that tracks status, milestones, dependencies, and risks across all active initiatives.

## Project Data Storage

Maintain project data in `.claude/projects.md` (create if it doesn't exist).

### File Structure

```markdown
# Project Portfolio

**Last updated:** [Date]
**Active projects:** [Count]
**At risk:** [Count]

---

## [Project Name]

**ID:** PRJ-[sequential number]
**Owner:** [Name]
**Sponsor:** [Executive sponsor]
**Status:** 🟢 On Track | 🟡 At Risk | 🔴 Blocked | ⚫ On Hold | ✅ Complete
**Priority:** P0 (Critical) | P1 (High) | P2 (Medium) | P3 (Low)
**Started:** [Date]
**Target completion:** [Date]
**Completion:** [X]%

### Objective
[One sentence — what does success look like?]

### Milestones
| Milestone | Target Date | Status | Actual Date | Notes |
|-----------|------------|--------|-------------|-------|
| ... | ... | Done/On Track/Late/Blocked | ... | ... |

### Dependencies
| Depends On | Type | Status | Impact if Delayed |
|-----------|------|--------|-------------------|
| [PRJ-X / External / Team] | Blocks / Informs | Clear / At Risk | [Description] |

### Risks
| Risk | Likelihood | Impact | Mitigation | Owner |
|------|-----------|--------|-----------|-------|
| ... | H/M/L | H/M/L | ... | ... |

### Recent Updates
- [Date]: [Update]
- [Date]: [Update]

### Key Decisions
- DEC-[X]: [Reference to decision log]

---
```

## Modes

### Mode 1: Dashboard View

Read `.claude/projects.md` and display:

#### Project Portfolio Dashboard — [Date]

| # | Project | Owner | Priority | Status | Completion | Next Milestone | Due | Risk |
|---|---------|-------|----------|--------|------------|----------------|-----|------|
| PRJ-1 | ... | ... | P0 | 🟢 | 75% | ... | ... | Low |
| PRJ-2 | ... | ... | P1 | 🟡 | 40% | ... | ... | Med |

**Summary:**
- **On track:** X projects
- **At risk:** X projects (list them with reason)
- **Blocked:** X projects (list them with blocker)
- **Decisions needed:** [List any pending decisions]

### Mode 2: Add New Project

Walk through the fields and create a new PRJ entry. Assign next sequential ID.

### Mode 3: Update Project

When user provides an update:
1. Read the project file
2. Update the relevant fields (status, completion %, milestones)
3. Add an entry to "Recent Updates"
4. Recalculate overall status based on milestones and risks
5. Write the updated file
6. Flag if status changed (especially if it degraded)

### Mode 4: Risk Review

Across all projects, surface:

#### Portfolio Risk Report

| Risk | Project | Likelihood | Impact | Risk Score | Mitigation Status |
|------|---------|-----------|--------|-----------|-------------------|
| ... | PRJ-X | H | H | Critical | In progress / Not started |

**Top 3 risks by impact:**
1. [Risk] — [What to do about it]
2. ...
3. ...

**Dependency chain risks:** [Projects that depend on at-risk projects]

### Mode 5: Dependency Map

Show cross-project dependencies:

```
PRJ-1 ──blocks──▶ PRJ-3
PRJ-2 ──blocks──▶ PRJ-3
PRJ-3 ──informs──▶ PRJ-5
PRJ-4 (independent)
```

Flag circular dependencies or long chains.

### Mode 6: Project Retrospective

When a project completes, generate:

#### Retrospective: [Project Name]

| Field | Details |
|-------|---------|
| **Planned duration** | X weeks |
| **Actual duration** | Y weeks (Z% over/under) |
| **Key milestones hit on time** | X of Y |
| **Risks that materialized** | [List] |
| **Risks that didn't** | [List] |

**What went well:**
- ...

**What didn't:**
- ...

**Lessons for next time:**
- ...

Mark project as ✅ Complete in the file.

## Principles

1. **One source of truth.** All project status lives in this file. No side channels.
2. **Status is earned, not declared.** 🟢 means milestones are on track, not "I feel good about it."
3. **Surface risks early.** A 🟡 with a mitigation plan is better than a false 🟢.
4. **Kill zombie projects.** If a project hasn't been updated in 2+ weeks, flag it.

## Input

$ARGUMENTS
