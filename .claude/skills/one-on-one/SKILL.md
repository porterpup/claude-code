---
name: one-on-one
description: Prep and manage recurring 1:1 meetings with direct reports or managers. Track goals, feedback, career development, and follow-ups across sessions.
allowed-tools: Read Grep Glob Bash Write Edit TodoWrite
argument-hint: [person's name, "prep for 1:1 with [name]", or "review history with [name]"]
---

# 1:1 Meeting Management

You manage the full lifecycle of recurring 1:1 meetings — prep, agenda, notes, and continuity across sessions. This goes beyond generic meeting-notes by maintaining persistent relationship context.

## 1:1 Data Storage — Context-Aware

1:1 records are namespaced by context:

```bash
CONTEXT=$(./scripts/context-path.sh)   # personal | 3cv | grantdrive
DIR=".claude/contexts/$CONTEXT/one-on-ones"
FILE="$DIR/[person-name].md"
```

- **Write mode:** Write to `.claude/contexts/[current-context]/one-on-ones/[name].md`.
- **Read mode (personal master):** Scan all `.claude/contexts/*/one-on-ones/`.
  When displaying the 1:1 portfolio, show a Context column.
- **Read mode (work instances):** Only your own context.

The same person may appear in multiple contexts (e.g., a 3CV colleague you also
meet with informally). Keep the files separate — the 3CV 1:1 is about work, the
personal 1:1 is about something else.

### File Structure

```markdown
# 1:1 with [Person Name]
**Role:** [Their role]
**Relationship:** [Direct report / Manager / Peer / Skip-level]
**Cadence:** [Weekly / Bi-weekly / Monthly]
**Preferred format:** [In-person / Video / Walking / Coffee]

## Standing Topics
- [Topic they always want to discuss]
- [Recurring theme]

## Goals & Development
| Goal | Timeline | Status | Last Discussed |
|------|----------|--------|---------------|
| ... | ... | ... | ... |

## Feedback Given
| Date | Topic | Feedback | Reception |
|------|-------|----------|-----------|
| ... | ... | ... | Well / Mixed / Poorly |

## Feedback Received
| Date | Topic | Feedback | My Action |
|------|-------|----------|-----------|
| ... | ... | ... | ... |

## Session Log

### [Date]
**Mood/energy:** [Observed]
**Topics discussed:**
- ...
**Action items:**
- [ ] [Action] — Owner: [name] — Due: [date]
**Follow up next time:**
- ...

---
```

## Modes

### Mode 1: Prep for Upcoming 1:1

Read the person's file and generate:

#### 1:1 Prep: [Name] — [Date]

**Last met:** [Date] | **Open action items:** [Count]

**Carry-forward items:**
- [ ] [Action from last time — status check]

**Suggested agenda:**
1. [Check in — how are they doing?]
2. [Follow up on X from last time]
3. [New topic based on recent events]
4. [Career/development check-in if due]
5. [Your items to share/discuss]

**Talking points:**
- [Specific praise or recognition to give]
- [Concern or feedback to raise]
- [Decision to communicate]

**Watch for:**
- [Pattern from recent sessions — e.g., "Mentioned burnout last 2 sessions"]
- [Goal milestone approaching]

### Mode 2: Log Session Notes

After a 1:1, the user provides notes or a summary. You:
1. Structure them into the session log format
2. Extract action items with owners and dates
3. Update goals if discussed
4. Update feedback given/received if applicable
5. Note carry-forward items for next session
6. Append to the person's file

### Mode 3: Review Relationship History

Summarize the arc of your 1:1 relationship:
- Sessions held (count, frequency adherence)
- Top recurring topics
- Open vs. completed action items (yours and theirs)
- Feedback patterns (what you've given, what you've received)
- Goal progress over time
- Relationship health indicators (engagement, trust signals)

### Mode 4: 1:1 Portfolio View

Show all active 1:1 relationships:

| Context | Person | Role | Cadence | Last Met | Next Due | Open Items | Health |
|---------|--------|------|---------|----------|----------|------------|--------|
| personal | ... | ... | ... | ... | ... | ... | 🟢/🟡/🔴 |
| 3cv | ... | ... | ... | ... | ... | ... | 🟢/🟡/🔴 |

Flag:
- Overdue 1:1s (missed cadence)
- People with many open action items (follow-through risk)
- People you haven't given feedback to recently

## Principles

1. **Consistency beats intensity.** Regular 30-minute 1:1s > sporadic 90-minute ones.
2. **Their agenda first.** The first half belongs to them.
3. **Track patterns, not just events.** Three mentions of "overwhelmed" = a trend.
4. **Close the loop.** Every action item from a 1:1 should be resolved or explicitly carried forward.

## Input

$ARGUMENTS
