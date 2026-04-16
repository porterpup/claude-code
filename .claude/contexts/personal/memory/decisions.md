# Decisions Memory (personal)

---

### 2026-04-16 Use Claude Code directly, not Slack, for solo ops on this sandbox
**Tags:** type:decision, domain:operations
**Content:** Slack runner pattern OOMs on 16GB sandbox — each `claude -p` subprocess peaks ~10-15GB. Use Claude Code sessions + subagents directly. Slack runner migration to Mac/launchd deferred.

---

### 2026-04-16 Search for skills first before custom-building
**Tags:** type:decision, domain:operations
**Content:** Before writing custom code, search skillsmp.com and skillstore.io first. gws CLI replaced a planned custom Gmail label MCP wrapper.

---

### 2026-04-16 Use gws CLI for Gmail write operations
**Tags:** type:decision, domain:operations
**Content:** Google Workspace MCP is read-only for Gmail. Use gws CLI (npm @googleworkspace/cli) for label/modify/trash. Credentials: /tmp/gws-creds.json (derived from MCP creds, ephemeral — rebuild on sandbox recycle). Env var: GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE=/tmp/gws-creds.json.

---

### 2026-04-16 Use Sonnet subagents for batch/routine work
**Tags:** type:decision, domain:operations
**Content:** Batch ops via Agent tool with model=sonnet. First inbox cleanup run: ~500 emails, 40k tokens, 12 min. Subagent context is isolated; only summary returns.

---
