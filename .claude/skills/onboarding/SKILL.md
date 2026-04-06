---
name: onboarding
description: Create onboarding plans for new hires, team members, or projects. Generate 30/60/90 day plans, welcome materials, and knowledge transfer documents.
allowed-tools: Read Grep Glob Bash TodoWrite
argument-hint: [role, team, project, or onboarding context]
---

# Onboarding & Knowledge Transfer

You create structured onboarding plans that get new team members productive quickly while building the relationships and context they need to succeed long-term.

## Mode 1: 30/60/90 Day Onboarding Plan

### Onboarding Plan: [Role/Name]
**Start Date:** [Date]
**Manager:** [Name]
**Buddy:** [Name]
**Team:** [Team]

---

#### Week 1: Orientation & Setup
**Goal:** Fully set up and oriented. Knows who to ask for what.

| Day | Focus | Activities | Owner |
|-----|-------|-----------|-------|
| 1 | Welcome | Welcome meeting, IT setup, tool access, office tour | Manager + IT |
| 2 | Context | Company overview, team structure, current priorities | Manager |
| 3 | People | 1:1s with immediate team members | Buddy |
| 4 | Process | Dev workflow, communication norms, meeting cadence | Buddy |
| 5 | First task | Small, well-scoped starter task to build confidence | Manager |

**Checklist:**
- [ ] All tool access granted (list specific tools)
- [ ] Added to relevant Slack channels / email lists
- [ ] Calendar populated with recurring meetings
- [ ] Org chart and key contacts shared
- [ ] Company handbook / docs shared

#### Days 8-30: Learn & Contribute
**Goal:** Understands the product/codebase. Completing tasks independently.

- [ ] Complete [X] onboarding tasks/tickets
- [ ] Shadow [key meetings/processes]
- [ ] 1:1s with cross-functional partners ([list names])
- [ ] Read key documentation: [list]
- [ ] Present a "What I've Learned" summary to team
- [ ] **30-Day Check-in:** Manager reviews progress, adjusts plan

**Success Metrics:**
- Can explain what the team does and why it matters
- Has merged [N] PRs / completed [N] tasks
- Knows the escalation path for issues

#### Days 31-60: Deepen & Own
**Goal:** Owns a workstream. Contributing to planning, not just execution.

- [ ] Take ownership of [specific area/feature]
- [ ] Lead or co-lead [a meeting or initiative]
- [ ] Identify one process improvement and propose it
- [ ] Expand network: 1:1s with [stakeholders outside team]
- [ ] **60-Day Check-in:** Discuss trajectory, interests, and growth areas

**Success Metrics:**
- Can independently handle [X type of work]
- Has proposed at least one improvement
- Peers would describe them as "ramped up"

#### Days 61-90: Lead & Impact
**Goal:** Fully productive. Making independent decisions. Visible impact.

- [ ] Lead a project or significant feature end-to-end
- [ ] Mentor or help onboard the next new hire
- [ ] Present work to broader team/stakeholders
- [ ] Write or improve documentation based on onboarding experience
- [ ] **90-Day Review:** Formal performance conversation, goal-setting

**Success Metrics:**
- Delivering at the level expected for the role
- Has built relationships across the organization
- Can articulate team strategy and their role in it

---

## Mode 2: Knowledge Transfer Document

When someone is transitioning out or handing off responsibilities:

### Knowledge Transfer: [Area/Role]
**From:** [Name] → **To:** [Name]
**Transition Date:** [Date]

#### Responsibilities Being Transferred
| Responsibility | Frequency | Priority | Current Status | Documentation |
|---------------|-----------|----------|---------------|---------------|
| ... | Daily/Weekly/Ad-hoc | H/M/L | [State] | [Link or "needs doc"] |

#### Key Contacts
| Who | For What | Relationship Notes |
|-----|----------|-------------------|
| ... | ... | [Context about the relationship] |

#### Active Projects / In-Flight Work
| Project | Status | Next Milestone | Key Decisions Pending |
|---------|--------|---------------|----------------------|
| ... | ... | ... | ... |

#### Tribal Knowledge (The Stuff That Isn't Written Down)
1. [Important context that only exists in someone's head]
2. [Workarounds, gotchas, "here's how this actually works"]
3. [Political dynamics or sensitivities to be aware of]

#### Access & Permissions Needed
- [ ] [System/tool] — [level of access]
- [ ] ...

#### Open Loops to Close
- [ ] [Thing that needs resolution before transition is complete]
- [ ] ...

## Input

$ARGUMENTS
