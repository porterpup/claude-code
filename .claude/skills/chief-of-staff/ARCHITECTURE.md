# Chief of Staff — Architecture

## Goals

1. The orchestrator's context window stays bounded as the swarm grows.
2. Specialists are stateless: spin up, do one job, write to Notion, exit.
3. The same agents work for both interactive use (in Claude Code) and unattended runs (cron).

## Components

```
                    ┌──────────────────────────────┐
                    │   You (terminal / web / phone)│
                    └──────────────┬────────────────┘
                                   │
                    ┌──────────────▼────────────────┐
                    │  /chief-of-staff (skill)      │  Sonnet
                    │  Orchestrator. Routes,        │
                    │  spawns subagents, reads      │
                    │  Notion to synthesize.        │
                    └──┬──────────────────────┬─────┘
                       │ Agent tool           │ mcp__notion (read)
              ┌────────▼─────┐      ┌─────────▼──────┐
              │  cos-inbox   │      │ cos-calendar   │  Sonnet, ephemeral
              │  (subagent)  │      │  (subagent)    │
              └────┬─────────┘      └────┬───────────┘
                   │ gws CLI             │ gws CLI
                   │ + mcp__notion       │ + mcp__notion (write)
                   ▼                     ▼
              ┌────────────────────────────────────┐
              │       Notion — Briefings DB        │
              │       (per teamspace)              │
              └────────────────────────────────────┘
                              ▲
                              │ cron triggers `claude -p` headless
                              │ to write briefings overnight
                  ┌───────────┴───────────┐
                  │ scripts/cron-*.sh     │
                  └───────────────────────┘
```

## Token strategy

| Layer | Why it stays small |
|-------|--------------------|
| Orchestrator | Never ingests specialist output verbatim. Specialists return ONE line; orchestrator queries Notion Briefings DB only when the user asks for detail. |
| Specialists | Fresh context per spawn. Read only their rules YAML + workspace map + the inbox/calendar slice they need. No conversation history. |
| Notion | Long-lived state. Briefings are queryable by `Source`, `Type`, `Status`, `Window`, so the orchestrator pulls only what's relevant. |
| Model tier | Sonnet for everyone today. Escalate orchestrator to Opus only if synthesis quality demands it (and only the orchestrator — specialists are mechanical and Sonnet handles them fine). |

## Two trigger surfaces

**Interactive (you in Claude Code).** `/chief-of-staff <request>` → orchestrator decides which specialists are needed → spawns them via the `Agent` tool with `subagent_type: cos-inbox` / `cos-calendar` (parallel when independent) → each returns one line → orchestrator pulls Briefings from Notion → synthesizes one answer for you.

**Unattended (cron).** `scripts/cron-morning-brief.sh` runs `claude -p "<prompt>"` headless. The prompt invokes the orchestrator the same way. Briefings land in Notion before you wake up. Next time you open Claude Code, the orchestrator finds them in `Status=fresh`.

## Notion schema additions

The existing bootstrap (`scripts/bootstrap-notion.py`) creates Projects, Tasks, Decisions, Stakeholders. The new bootstrap (`scripts/bootstrap-notion-briefings.py`) adds **one** database per teamspace:

**Briefings**
- `Name` (title)
- `Source` (select: cos-inbox, cos-calendar, manual)
- `Type` (select: triage, preview, task-proposal, draft-proposal, cleanup, meeting-prep, schedule-audit, find-time, daily-digest, weekly-summary)
- `Window` (rich_text)
- `Status` (select: fresh, consumed, stale)
- `Created` (created_time)
- `Related Tasks` (relation → Tasks)
- `Related Projects` (relation → Projects)

`Status=fresh` until the orchestrator surfaces it to the user, then it flips to `consumed`. A weekly job (or manual sweep) marks anything older than 7 days `stale`.

## Failure modes & guardrails

- **Specialist returns >1 line.** Orchestrator should warn but not crash. Treat the first line as the pointer.
- **Specialist fails to write Notion.** It returns `cos-X: ERROR notion-write-failed: <body>`. Orchestrator surfaces verbatim — does NOT retry the whole specialist.
- **Notion is down.** Orchestrator falls back to telling the user "Briefings unavailable" rather than fabricating a synthesis.
- **Specialist over-runs the inbox safety cap (>100 emails).** Hard-coded refusal in the specialist. Orchestrator must explicitly re-invoke with `--allow-bulk` (not implemented yet — design TBD).

## Adding a new specialist

1. Drop `.claude/agents/cos-<thing>.md` with the same shape as cos-inbox: boot sequence → tool policy → safety rules → commands → Briefing output → return value.
2. Add the source name to the `Source` select options in the Briefings DB (Notion auto-extends selects, so this happens implicitly on first write).
3. Mention the new specialist in `chief-of-staff/SKILL.md` so the orchestrator knows to route to it.

That's it. No runner process, no Slack app, no manifest. Just a markdown file and a Notion bootstrap row.
