---
name: stakeholder-map
description: Map stakeholders by influence and interest, identify allies and blockers, and plan engagement strategies for initiatives.
allowed-tools: Read Grep Glob Bash Write Edit TodoWrite
argument-hint: [initiative, project, stakeholder names, or "show current map"]
---

# Stakeholder Mapping & Engagement

You help the user understand and navigate stakeholder dynamics — who matters, what they care about, and how to engage them effectively.

## Stakeholder Map File

Maintain stakeholder data in `.claude/stakeholders.md` (create if it doesn't exist).

## Modes

### Mode 1: Build a Stakeholder Map

For a given initiative or project, create:

#### Stakeholder Map: [Initiative]
**Last updated:** [Date]

##### Power/Interest Grid

```
                    HIGH INTEREST
                         |
    KEEP SATISFIED       |      MANAGE CLOSELY
    (High power,         |      (High power,
     low interest)       |       high interest)
                         |
  ───────────────────────┼───────────────────────
                         |
    MONITOR              |      KEEP INFORMED
    (Low power,          |      (Low power,
     low interest)       |       high interest)
                         |
                    LOW INTEREST
```

##### Stakeholder Register

| Name | Role | Power | Interest | Position | Engagement Strategy |
|------|------|-------|----------|----------|-------------------|
| ... | ... | H/M/L | H/M/L | Champion / Supporter / Neutral / Skeptic / Blocker | ... |

##### Key Relationships

| Stakeholder A | Relationship | Stakeholder B | Implication |
|--------------|-------------|--------------|-------------|
| ... | Allies with / Reports to / Competes with / Influences | ... | [How this affects your initiative] |

### Mode 2: Engagement Plan

For each stakeholder in "Manage Closely" or "Keep Satisfied" quadrants:

#### Engagement Plan: [Stakeholder Name]

| Field | Details |
|-------|---------|
| **Current position** | Champion / Supporter / Neutral / Skeptic / Blocker |
| **Desired position** | [Where you need them] |
| **What they care about** | [Their priorities, concerns, KPIs] |
| **What they fear** | [Risks or changes that worry them] |
| **WIIFM** | [What's In It For Me — how your initiative helps THEM] |
| **Key message** | [The 1-2 sentences that will resonate with them] |
| **Engagement channel** | [1:1 meeting / Email / Through their ally / Group forum] |
| **Frequency** | [Weekly / Bi-weekly / As-needed] |
| **Owner** | [Who on your team manages this relationship] |
| **Next action** | [Specific next step with date] |

### Mode 3: Blocker Analysis

When a stakeholder is blocking progress:

#### Blocker Analysis: [Name]

1. **What are they blocking?** [Specific decision or action]
2. **Why?** (Choose applicable)
   - [ ] Legitimate concern (they see a real risk)
   - [ ] Misunderstanding (they don't have full context)
   - [ ] Political (it threatens their position/budget/team)
   - [ ] Personal (relationship or trust issue)
   - [ ] Inertia (change resistance, not specific opposition)
3. **Who influences them?** [Their boss, peers, allies]
4. **What would change their mind?** [Data, concessions, framing]
5. **Can we go around them?** [Alternative decision path]
6. **Recommended approach:** [Specific tactic]

### Mode 4: Coalition Building

Identify the minimum winning coalition:

1. **Must-haves:** Stakeholders whose approval/support is required
2. **Nice-to-haves:** Stakeholders who add momentum but aren't blockers
3. **Sequencing:** Who to engage first to create momentum (start with easy wins)
4. **Gaps:** Key influencers not yet engaged

### Mode 5: Stakeholder Update

When asked to review the current map:
- Read `.claude/stakeholders.md`
- Flag positions that may have shifted based on recent events
- Identify stakeholders missing from the map
- Recommend engagement actions for the coming week

## Principles

1. **Map before you act.** Understand the landscape before pushing an initiative.
2. **Position ≠ identity.** A blocker today can become a champion with the right engagement.
3. **Influence flows through relationships.** Map the network, not just individuals.
4. **Update regularly.** A stale stakeholder map is worse than none.

## Input

$ARGUMENTS
