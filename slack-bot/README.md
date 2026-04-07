# Chief of Staff Slack Bot

A Slack bot that gives you chat access to your AI Chief of Staff suite (19 skills + MCP integrations) from Slack.

Built on:
- **Slack Bolt for Python** with Socket Mode (no public URL required)
- **Claude Agent SDK** for Python
- Your existing `.claude/skills/` and `.mcp.json` in the parent repo

## What it does

- DM the bot or mention it in a channel
- It invokes Claude with your full skill suite available
- Responses stream back to Slack
- Access control via Slack user ID allowlist

## Setup

### 1. Create a Slack app

1. Go to https://api.slack.com/apps → **Create New App** → **From scratch**
2. Name it (e.g., "Chief of Staff") and pick your workspace
3. **Socket Mode** → Enable → Generate an **App-Level Token** with scope `connections:write`. Save it (starts with `xapp-`).
4. **OAuth & Permissions** → Add these Bot Token Scopes:
   - `app_mentions:read`
   - `chat:write`
   - `im:history`
   - `im:read`
   - `im:write`
   - `channels:history` (only if you want channel access)
5. **Event Subscriptions** → Enable → Subscribe to bot events:
   - `app_mention`
   - `message.im`
6. **Install App** to your workspace. Copy the **Bot User OAuth Token** (starts with `xoxb-`).

### 2. Install dependencies

```bash
cd slack-bot
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure environment

Copy `.env.example` to `.env` and fill in:

```bash
cp .env.example .env
```

```
SLACK_BOT_TOKEN=xoxb-...
SLACK_APP_TOKEN=xapp-...
ANTHROPIC_API_KEY=sk-ant-...
ALLOWED_SLACK_USER_IDS=U01ABC123,U02DEF456
CLAUDE_PROJECT_DIR=/home/user/claude-code
```

`ALLOWED_SLACK_USER_IDS` is comma-separated — only these users can talk to the bot. Find your Slack user ID by clicking your profile → More → Copy member ID.

### 4. Run

```bash
python bot.py
```

You should see `⚡️ Bolt app is running!` — now DM the bot in Slack.

## Running as a service (optional)

See `systemd/cos-slack-bot.service` for a systemd user unit to keep it running.

```bash
mkdir -p ~/.config/systemd/user
cp systemd/cos-slack-bot.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now cos-slack-bot
systemctl --user status cos-slack-bot
```

## Security notes

- The bot runs with `permission_mode="default"` — Claude will use tools from MCP servers (Gmail, Outlook, Jira, Trello) based on what you ask. Tools that send email or create tickets WILL execute. Be deliberate about what you ask it to do.
- Only users in `ALLOWED_SLACK_USER_IDS` can interact.
- Never commit `.env` — it's gitignored.
