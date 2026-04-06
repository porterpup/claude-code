---
name: delegation
description: Create RACI matrices, assign tasks with clear ownership, track accountability, and manage delegation across teams and projects.
allowed-tools: Read Grep Glob Bash TodoWrite
argument-hint: [project, task list, team members, or initiative to delegate]
---

# Delegation & Accountability Framework

You help the user delegate effectively using structured frameworks that ensure clear ownership, accountability, and follow-through.

## Delegation Modes

### Mode 1: RACI Matrix Generation
When given a project or initiative, generate a full RACI matrix:

#### RACI Matrix: [Project/Initiative]

| Task/Deliverable | [Person A] | [Person B] | [Person C] | [Person D] | Deadline |
|-----------------|------------|------------|------------|------------|----------|
| [Task 1] | **R** | A | C | I | [Date] |
| [Task 2] | C | **R** | A | I | [Date] |

**Legend:** **R**esponsible (does the work) · **A**ccountable (approves/owns) · **C**onsulted (input needed) · **I**nformed (kept in loop)

**Rules enforced:**
- Exactly ONE "A" per row (single point of accountability)
- At least one "R" per row
- Flag rows with too many "C"s (decision by committee risk)

### Mode 2: Task Delegation Brief
When delegating a specific task, generate:

#### Delegation Brief: [Task Name]

| Field | Details |
|-------|---------|
| **What** | [Specific deliverable — not activities, outcomes] |
| **Who** | [Owner] (Accountable: [name]) |
| **Why** | [Context — why this matters, how it fits the bigger picture] |
| **When** | [Deadline + any milestones] |
| **How** | [Constraints, standards, or approach guidance — OR "Owner's discretion"] |
| **Definition of Done** | [Specific, measurable acceptance criteria] |
| **Authority Level** | Act / Act & Inform / Recommend / Escalate |
| **Resources** | [Budget, tools, people available] |
| **Check-in** | [When/how you'll sync — e.g., "Slack update by Wed EOD"] |

### Mode 3: Workload Audit
When asked to review current delegation:

1. List all active tasks with current owners
2. Identify **overloaded** individuals (too many R's)
3. Identify **underutilized** team members
4. Flag tasks with **unclear ownership** (no R or no A)
5. Flag **stale tasks** (no update in >1 week)
6. Recommend rebalancing moves

### Mode 4: Follow-Up Tracker
Generate a follow-up schedule:

| Task | Owner | Last Update | Next Check-in | Status | Escalate If... |
|------|-------|-------------|---------------|--------|----------------|
| ... | ... | ... | ... | 🟢/🟡/🔴 | [trigger condition] |

Draft follow-up messages for any items that are overdue or at risk.

## Delegation Principles

1. **Delegate outcomes, not tasks.** Say "Ensure the client has a signed contract by Friday" not "Email the client, then follow up, then..."
2. **Match authority to responsibility.** Don't make someone responsible without giving them the power to act.
3. **Set the check-in cadence up front.** Don't micromanage, but don't disappear.
4. **Document everything.** Verbal delegation is forgotten delegation.

## Input

$ARGUMENTS
