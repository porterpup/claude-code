# General Memory (personal)

---

### 2026-04-16 Infrastructure state
**Tags:** type:context, domain:operations
**Content:** gws Gmail label IDs: Label_18=Newsletters/Unsorted, Label_19=Financial/Receipts, Label_20=Inbox/Action, Label_21=Newsletters/Marketing, Label_22=Action/Airbnb, Label_23=Work/GrantDrive, Label_24=Triaged/Backlog, Label_25=Work/3CV, Label_26=Action/Calendar, Label_27=Financial/Banking, Label_28=Career/Recruiters, Label_29=Meetings/Recordings, Label_30=Inbox/FYI. Inbox cleanup: ~505 processed (first run), ~200-400 remain, 8 trashed (scam .top/.blog domains). Next: spawn another Sonnet subagent to finish remaining + re-classify 50 batch-6 messages (Triaged/Backlog only, no category label). Triage rules: /home/user/claude-code/slack-agents/triage-rules/personal.yaml.

---

### 2026-04-16 Sandbox constraints
**Tags:** type:context, domain:operations
**Content:** 16GB RAM, no swap. claude -p subprocess OOMs. Runners (slack-agents/runner.py) die on sandbox recycle — restart with ./slack-agents/start-runners.sh. /tmp is ephemeral. gws-creds.json rebuild: python3 script converts MCP creds (has refresh_token, client_id, client_secret) to authorized_user format. Long-term: launchd on Mac for persistent scheduled agents.

---
