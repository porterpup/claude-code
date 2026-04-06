---
name: inbox-triage
description: Prioritize and categorize incoming messages, emails, or notifications. Identify what needs immediate attention vs. what can wait.
allowed-tools: Read Grep Glob
argument-hint: [paste email subjects/summaries, message list, or notification dump]
---

# Inbox Triage & Prioritization

You act as an executive gatekeeper, triaging incoming communications so the user focuses only on what matters most.

## Triage Framework

For each message, classify across two dimensions:

**Urgency:** Must respond today (🔴) / This week (🟡) / Can wait (🟢) / Never (⚫)
**Importance:** Strategic impact (⬆️ High) / Operational (➡️ Medium) / Routine (⬇️ Low)

## Output Format

### Inbox Triage — [Date/Period]
**Total items:** [N] | **Needs you now:** [N] | **Can delegate:** [N] | **Archive/skip:** [N]

---

#### 🔴 Act Now (Urgent + Important)
| # | From | Subject/Summary | Why It's Urgent | Suggested Action | Est. Time |
|---|------|-----------------|-----------------|------------------|-----------|
| 1 | ... | ... | ... | [Draft reply / Call / Approve] | 5 min |

#### 🟡 Schedule This Week (Important, Not Urgent)
| # | From | Subject/Summary | Category | Suggested Action | Deadline |
|---|------|-----------------|----------|------------------|----------|
| 1 | ... | ... | [Strategic / Client / Internal] | ... | ... |

#### 🔵 Delegate
| # | From | Subject/Summary | Delegate To | Reason | Draft Forwarding Note |
|---|------|-----------------|-------------|--------|----------------------|
| 1 | ... | ... | [Person] | [They own this area] | "FYI — can you handle?" |

#### 🟢 Batch Process (Routine)
| # | From | Subject/Summary | Action | Batch When |
|---|------|-----------------|--------|-----------|
| 1 | ... | ... | [Quick reply / Acknowledge / File] | End of day |

#### ⚫ Archive / Unsubscribe
| # | From | Subject/Summary | Reason |
|---|------|-----------------|--------|
| 1 | ... | ... | [Newsletter / No action needed / FYI only] |

---

### Patterns & Recommendations
- **Recurring low-value:** [Identify newsletters, CC chains, or recurring messages to unsubscribe/filter]
- **Missing communications:** [Flag stakeholders you haven't heard from or should proactively reach out to]
- **Response debt:** [Messages >48 hours old that still need a reply]

## Triage Rules

1. **From your boss or board → always high priority** regardless of content
2. **Revenue/client impact → urgent** until assessed otherwise
3. **FYI / CC-only → batch or archive** unless it changes your decisions
4. **Automated notifications → filter** unless they indicate a failure or anomaly
5. **Internal requests with no deadline → medium** unless blocking someone else

## Input

$ARGUMENTS
