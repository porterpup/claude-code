# Slack Agent Swarm

Multi-agent Claude team that lives in `#cos` on `grovestreetholdings.slack.com`.
Each agent is a distinct Slack app (different name, avatar) so the channel
reads like a team, not one bot talking to itself.

## Agents

| Agent         | Role                                                  | App Manifest                |
| ------------- | ----------------------------------------------------- | --------------------------- |
| `@cos`        | Orchestrator. You talk to it; it delegates.           | `manifests/cos.yaml`        |
| `@cos-notion` | Specialist. Does Notion ops when delegated by `@cos`. | `manifests/cos-notion.yaml` |

## Architecture

- **Ephemeral invocation model**: each `@mention` spawns a short-lived Claude
  Agent SDK session, runs one turn, posts a response, exits.
- **Strict addressing**: an agent only responds if its `@handle` is in the
  message. Prevents infinite bot-to-bot loops.
- **Runner process**: one Python process per agent holds a Socket Mode
  websocket, handles events, spawns Claude sessions. Runs in the sandbox for
  now; migrate to Fly.io / similar when we outgrow that.

## Setup — creating the apps

For each manifest in `manifests/`:

1. Go to <https://api.slack.com/apps> → **Create New App** → **From a manifest**
2. Pick workspace: **grovestreetholdings**
3. Paste the YAML from the file
4. Click **Create**
5. On the app page: **Install to Workspace** → Allow
6. **Basic Information → App-Level Tokens → Generate Token and Scopes**:
   - Token Name: `socket`
   - Scope: `connections:write`
   - Copy the `xapp-...` token
7. **OAuth & Permissions**: copy the `xoxb-...` Bot User OAuth Token
8. In `#cos` on Slack: `/invite @cos` (or `/invite @cos-notion`)

Paste both tokens for both apps back here and the runner will be wired.

## Tokens

Stored in `.env.slack` (gitignored). Never committed.

```
COS_BOT_TOKEN=xoxb-...
COS_APP_TOKEN=xapp-...
COS_NOTION_BOT_TOKEN=xoxb-...
COS_NOTION_APP_TOKEN=xapp-...
```
