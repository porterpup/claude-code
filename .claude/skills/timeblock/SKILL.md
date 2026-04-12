---
name: timeblock
description: Daily time-block planning using Cal Newport's method. Generate plans, handle replanning, review days, and protect deep work. Integrates with your calendar and task list.
allowed-tools: Read Grep Glob Bash Write Edit TodoWrite
argument-hint: ["plan today", "plan tomorrow", "replan from [time]", "review today", "show current plan", or paste calendar/task data]
---

# Time-Block Planner — Cal Newport Method

You implement Cal Newport's time-blocking methodology as a daily planning tool.
Every minute of the workday gets assigned a job. The goal is NOT rigidity — it's
intentionality. When the plan breaks (and it will), you replan.

## Core Philosophy

> "Your goal is not to stick to a given schedule at all costs; it's instead to
> maintain a thoughtful say in what you're doing with your time going forward."
> — Cal Newport

## Plan Storage

Maintain daily plans in `.claude/timeblock/YYYY-MM-DD.md` (create directory if needed).

## Plan Format

Each daily plan uses this structure:

```markdown
# Time-Block Plan — [Day, Month DD, YYYY]

## Today's Deep Work Target
[1-2 sentences: what is the MOST IMPORTANT cognitively demanding work today?]

## Plan (Version [N])

| Time        | Block                          | Notes / Actual |
|-------------|--------------------------------|----------------|
| 08:00-08:30 | ☀️ Morning startup / plan day  |                |
| 08:30-10:00 | 🔴 DEEP: [task]               |                |
| 10:00-10:15 | ☕ Break                        |                |
| 10:15-11:00 | 🔴 DEEP: [task continued]      |                |
| 11:00-11:30 | 🟡 SHALLOW: [batch tasks]      | - reply to X   |
|             |                                | - approve Y    |
|             |                                | - review Z     |
| 11:30-12:00 | 📅 Meeting: [name]             |                |
| 12:00-12:45 | 🍽️ Lunch                       |                |
| 12:45-14:00 | 🔴 DEEP: [task]               |                |
| 14:00-14:30 | 📅 Meeting: [name]             |                |
| 14:30-15:00 | ⬜ OVERFLOW / catch-up          |                |
| 15:00-16:00 | 🔴 DEEP: [task]               |                |
| 16:00-16:30 | 🟡 SHALLOW: [admin batch]      |                |
| 16:30-17:00 | 📋 Shutdown ritual             |                |

## Task Bank (unscheduled)
- [ ] [task not yet placed]
- [ ] [task not yet placed]

## End-of-Day Review
**Plan adherence:** [X of Y blocks completed as planned]
**Deep work hours achieved:** [N] / Target: [N]
**What broke the plan:** [brief]
**Tomorrow's carry-forward:** [tasks to move]
**Lessons:** [time estimates off? recurring interruption pattern?]
```

## Block Types

| Icon | Type | Rules |
|------|------|-------|
| 🔴 | **Deep Work** | Minimum 60 min. No email, Slack, or meetings during these. Protect at all costs. |
| 🟡 | **Shallow Work** | Batch small tasks (<15 min each) into 30-min blocks. List sub-tasks in Notes column. |
| 📅 | **Meetings** | Fixed — plan around these. Include 5-min buffer before/after. |
| ⬜ | **Overflow** | Conditional block: do task X if available, otherwise absorb spillover from previous block. |
| ☕/🍽️ | **Break** | Non-negotiable. Never skip. Schedule explicitly or they won't happen. |
| 📋 | **Shutdown** | End-of-day ritual: review plan, prep tomorrow, close all loops, hard stop. |

## Modes

### Mode 1: Plan Today / Plan Tomorrow

**Inputs needed (gather from context or ask):**
1. What hours are you working today? (default: 8:00-17:00)
2. What meetings are already on the calendar? (check MCP calendar tools if available)
3. What are today's top priorities? (check project-tracker, Jira, Trello if available)
4. How much deep work do you need? (default: minimum 3 hours)

**Planning rules:**
1. **Deep work goes first** — schedule the most cognitively demanding work in your peak hours (usually morning). Block at least 60-90 min continuously.
2. **Batch shallow work** — group all email, Slack, admin into 2-3 dedicated blocks. Never let them leak into deep work time.
3. **30-minute minimum** — no block shorter than 30 min. Smaller tasks get batched.
4. **Overflow blocks** — after every uncertain-duration deep work block, add an overflow/conditional block. If the deep work finishes on time, do the overflow task. If not, the overflow absorbs the spillover.
5. **Conservative estimates** — add 50% buffer to your first instinct for how long something takes.
6. **Every minute has a job** — no unassigned gaps. Even "buffer" is an assignment.
7. **Schedule breaks explicitly** — they don't happen automatically.
8. **Shutdown ritual** — last 30 min of day is always shutdown (review, prep tomorrow, hard stop).

**Output:** Write the full plan to `.claude/timeblock/YYYY-MM-DD.md`

### Mode 2: Replan

When the plan breaks (it will), the user says "replan from [time]" or "things changed":

1. Read the current plan from `.claude/timeblock/YYYY-MM-DD.md`
2. Mark completed blocks with ✅ in the Notes column
3. Note what happened (interruption, meeting ran long, new urgent task)
4. **Redraw the remaining day** from the current time forward
5. Reassess priorities: what still matters? What can be cut or moved to tomorrow?
6. Increment the version number (Plan Version 2, 3, etc.)
7. Write the updated plan back to the file

**Key principle:** Replanning is expected and healthy. A day with 3 replans is still a successful time-blocked day — you maintained intentionality throughout.

### Mode 3: Review Today

At end of day (or when asked), generate the End-of-Day Review section:

1. Read the plan file
2. Calculate:
   - Blocks completed vs. planned
   - Actual deep work hours
   - Number of replans needed
   - Tasks carried forward
3. Identify patterns:
   - Consistent time estimation errors
   - Recurring interruption sources
   - Times of day that consistently break
4. Generate lessons and carry-forward list
5. Append the review to the plan file

### Mode 4: Weekly Deep Work Audit

When asked for a weekly review, scan all `.claude/timeblock/` files for the week:

| Day | Deep Hours Target | Deep Hours Actual | Blocks Hit | Replans | Top Disruptor |
|-----|-------------------|-------------------|------------|---------|---------------|
| Mon | 4h | 3.5h | 8/10 | 2 | Meeting overrun |
| Tue | ... | ... | ... | ... | ... |
| **Week** | **20h** | **17h** | **85%** | **avg 2.2** | **Meetings** |

**Trend:** Deep work trending up/down/flat vs. last week.
**Recommendation:** [e.g., "Block Friday AM as no-meeting focus time"]

### Mode 5: Show Current Plan

Read and display today's plan from `.claude/timeblock/YYYY-MM-DD.md`.
Highlight the current time block based on system time.
Show what's coming next.

## Integration Points

- **Calendar** (`/calendar-prep`): Pull actual meetings to seed the plan
- **Project Tracker** (`/project-tracker`): Pull priorities for deep work blocks
- **Jira/Trello** (MCP): Pull sprint tasks to assign to blocks
- **Memory** (`/memory`): Store time-blocking preferences (work hours, peak hours, meeting-free days)

## Preferences to Learn

Over time, store these in memory:
- User's work hours (e.g., 8:00-17:30)
- Peak deep work hours (e.g., "mornings before 11")
- Meeting-free days (e.g., "no meetings Wednesday")
- Deep work hour target per day (e.g., "4 hours minimum")
- Common batched tasks (e.g., "email + Slack + expense reports = shallow block")

## Input

$ARGUMENTS
