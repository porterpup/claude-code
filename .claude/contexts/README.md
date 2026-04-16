# Contexts — Multi-Instance Data Namespacing

This Chief of Staff runs across **three contexts**, each with its own
credentials, MCP config, and data namespace. All contexts share the same
skills, but data is isolated per context. The **personal master** has a
unified view across all three.

## The Three Contexts

| Context | Who / Where | Uses | Runs On |
|---------|-------------|------|---------|
| `personal` | You, at home | Personal Gmail, Google Calendar, personal Slack | Personal Claude (API key) |
| `3cv` | Your W2 job at 3CV | 3CV systems (work Slack, work backlog) | 3CV Claude (no API key needed) |
| `grantdrive` | Grant Drive activities | Outlook (MS365), Grant Drive calendar | Grant Drive Claude |

## Directory Structure

```
.claude/
├── skills/                    # Shared — identical across all contexts
├── current-context            # One-line file: "personal" | "3cv" | "grantdrive"
├── contexts/
│   ├── personal/              # Personal data
│   │   ├── decisions.md
│   │   ├── projects.md
│   │   ├── stakeholders.md
│   │   ├── one-on-ones/
│   │   ├── timeblock/
│   │   └── memory/
│   ├── 3cv/                   # 3CV work data (same structure)
│   └── grantdrive/            # Grant Drive data (same structure)
└── ...
```

## Data Flow

```
   3CV Instance              Grant Drive Instance          Personal Master
   ─────────────            ──────────────────────        ──────────────────
   context/3cv branch       context/grantdrive branch     main branch
                                                          
   Writes to                Writes to                     Reads from ALL
   contexts/3cv/*           contexts/grantdrive/*         contexts/*/ and
                                                          merges for unified
   git push ──────►                                       "what's on my plate?"
                            git push ──────►              view
                                                          ◄─── git fetch --all
```

## How Skills Use Context

Skills detect the current context by reading `.claude/current-context`,
defaulting to `personal` if absent. They then namespace their reads and writes:

- **Write mode:** Always writes to `contexts/[current-context]/...`
- **Read mode (non-personal):** Reads only from `contexts/[current-context]/...`
- **Read mode (personal master):** Reads from all `contexts/*/...` and merges,
  labeling each entry with its source context.

## Isolation Boundary

| Instance | Can See |
|----------|---------|
| Personal master | All contexts (personal + 3cv + grantdrive) |
| 3CV instance | Only `skills/` and `contexts/3cv/` |
| Grant Drive instance | Only `skills/` and `contexts/grantdrive/` |

Work instances check out **branches that don't contain personal data**:
- `context/3cv` branch — has `.claude/skills/` and `.claude/contexts/3cv/` only
- `context/grantdrive` branch — has `.claude/skills/` and `.claude/contexts/grantdrive/` only

## Switching Contexts

```bash
./scripts/switch-context.sh personal
./scripts/switch-context.sh 3cv
./scripts/switch-context.sh grantdrive
```

This:
1. Updates `.claude/current-context`
2. Copies `.mcp.[context].json` → `.mcp.json`
3. Echoes confirmation

## Syncing Contexts (Personal Master Only)

Run on the personal master to pull in the latest work data:

```bash
./scripts/sync-contexts.sh
```

This:
1. Fetches all `context/*` branches
2. Checks out each context's `.claude/contexts/[name]/` tree into `main`
3. Commits the merge to `main`

## MCP Config — Templates vs. Real Files

Credentials never live in git. The scheme:

| File | In Git? | Has Creds? | Purpose |
|------|---------|------------|---------|
| `.mcp.personal.json.template` | ✅ | No | Committed blueprint with empty credential fields |
| `.mcp.personal.json` | ❌ (gitignored) | Yes | Local file with real credentials, per-machine |
| `.mcp.json` | ❌ (gitignored) | Yes | Active copy, written by `switch-context.sh` |

Same pattern for `3cv` and `grantdrive`.

**First-time setup on a new machine:**
```bash
./scripts/switch-context.sh personal      # If .mcp.personal.json doesn't exist,
                                           # this copies the template and exits.
# Edit .mcp.personal.json with your real credentials.
./scripts/switch-context.sh personal      # Run again — now it activates.
```

**Why not env vars?** MCP server configs in Claude Code don't do env substitution reliably. The per-context JSON file is the simplest thing that works.
