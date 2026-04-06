---
name: memory
description: Persistent AI memory across sessions using memvid. Store, search, and recall decisions, stakeholder context, meeting outcomes, preferences, and any knowledge.
allowed-tools: Read Grep Glob Bash Write Edit TodoWrite
argument-hint: ["remember [fact]", "recall [topic]", "who is [person]", "what did we decide about [topic]", "memory status"]
---

# Persistent Memory — Chief of Staff Knowledge Base

You maintain long-term memory across sessions using memvid (preferred) or markdown files (fallback). This enables continuity — you remember decisions, people, preferences, and context from prior conversations.

## Memory Storage

**Primary (memvid):** `~/.chief-of-staff/memory.mv2`
**Fallback (markdown):** `.claude/memory/` directory with categorized `.md` files

On first use, check if memvid is available:
```bash
command -v memvid && echo "memvid available" || echo "memvid not installed"
```

If memvid is not installed, use the markdown fallback. Never fail silently — tell the user which backend you're using.

## Memvid Backend

### Store a Memory

```bash
echo "[content]" | memvid put ~/.chief-of-staff/memory.mv2 \
  --title "[short title]" \
  --tag "type:[decision|stakeholder|meeting|preference|action|context]" \
  --tag "domain:[finance|engineering|people|strategy|operations|other]" \
  --tag "project:[project-name]"
```

**Always tag with at least `type` and `domain`.** This enables precise filtering later.

### Search Memories

```bash
# Hybrid search (best for most queries)
memvid find ~/.chief-of-staff/memory.mv2 --query "[search terms]" --json

# Lexical search (exact matches, tag filtering)
memvid find ~/.chief-of-staff/memory.mv2 --query "[exact terms]" --mode lex --json

# Semantic search (conceptual similarity)
memvid find ~/.chief-of-staff/memory.mv2 --query "[concept]" --mode sem --json

# Time-filtered search
memvid find ~/.chief-of-staff/memory.mv2 --query "[topic]" --as-of-ts "[YYYY-MM-DD]" --json
```

### Entity/Stakeholder State

```bash
# Get everything known about a person or entity
memvid state ~/.chief-of-staff/memory.mv2 "[Person Name]"

# Timeline of interactions
memvid timeline ~/.chief-of-staff/memory.mv2
```

### Memory Maintenance

```bash
# Stats
memvid info ~/.chief-of-staff/memory.mv2

# Verify integrity
memvid verify ~/.chief-of-staff/memory.mv2

# Encrypt (if handling sensitive data)
memvid lock ~/.chief-of-staff/memory.mv2
```

## Markdown Fallback Backend

If memvid is unavailable, use structured markdown files:

```
.claude/memory/
  decisions.md      # Decision log entries
  stakeholders.md   # People and relationship context
  preferences.md    # User preferences, working style, recurring instructions
  meetings.md       # Meeting outcomes and follow-ups
  projects.md       # Project context and status
  general.md        # Everything else
```

Each entry format:
```markdown
### [YYYY-MM-DD] [Title]
**Tags:** type:decision, domain:finance
**Context:** [Brief context]
**Content:** [The actual information to remember]
---
```

Search via Grep across all files in `.claude/memory/`.

## Modes

### Mode 1: Remember (Store)
When the user says "remember this", "note that", or you encounter important information:

1. Classify the memory (type + domain)
2. Extract key entities (people, projects, dates)
3. Store with appropriate tags
4. Confirm what was stored: "Noted: [summary]. Tagged as [tags]."

**Auto-store triggers** — Always offer to remember:
- Decisions made during conversation
- Stakeholder preferences or context shared
- User preferences about how they like things done
- Action item outcomes
- Meeting takeaways

### Mode 2: Recall (Search)
When the user asks "what do we know about...", "remind me...", or you need context:

1. Search memory with the most relevant query
2. Present findings with dates and source context
3. Flag if information might be stale (>30 days old)

### Mode 3: Who Is (Entity Lookup)
When asked about a person:

1. Use `memvid state` (or grep stakeholders.md)
2. Present structured profile:
   - Role, organization, relationship
   - Last interaction
   - Key preferences or notes
   - Open action items involving them

### Mode 4: Memory Status
Show memory health:
- Total memories stored
- Breakdown by type and domain
- Oldest and newest entries
- Storage size
- Backend in use (memvid vs. markdown)

### Mode 5: Session Start Context Load
At the start of a conversation, if the user's query relates to a known topic:
1. Proactively search memory for relevant context
2. Briefly surface key context: "Based on previous sessions, I recall that..."
3. Don't overwhelm — 2-3 most relevant memories max

## Memory Hygiene Rules

1. **Be selective.** Not everything is worth remembering. Focus on decisions, people, preferences, and commitments.
2. **Date everything.** Memory without timestamps is unreliable.
3. **Tag consistently.** Use the predefined type/domain tags.
4. **Flag staleness.** Memories older than 90 days should be treated as "might have changed."
5. **Never store secrets.** No passwords, API keys, tokens, or PII beyond names and roles.

## First-Time Setup

If `~/.chief-of-staff/memory.mv2` doesn't exist:

```bash
mkdir -p ~/.chief-of-staff
memvid create ~/.chief-of-staff/memory.mv2
echo "Chief of Staff memory initialized on $(date)" | memvid put ~/.chief-of-staff/memory.mv2 --title "System: Memory Initialized" --tag "type:context"
```

If memvid is not installed, create the markdown fallback:
```bash
mkdir -p .claude/memory
for f in decisions stakeholders preferences meetings projects general; do
  echo "# ${f^} Memory\n\n---\n" > ".claude/memory/${f}.md"
done
```

## Input

$ARGUMENTS
