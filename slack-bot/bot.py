"""Chief of Staff Slack Bot.

A Slack bot that bridges Slack messages to the Claude Agent SDK, giving you
chat access to your full Chief of Staff skill suite and MCP integrations.

Architecture:
    Slack (Socket Mode) -> Slack Bolt handler -> Claude Agent SDK -> Claude
                                                      |
                                                      v
                                        .claude/skills/ + .mcp.json
                                        (Gmail, MS365, Jira, Trello, ...)
"""

from __future__ import annotations

import asyncio
import logging
import os
from pathlib import Path

from claude_agent_sdk import ClaudeAgentOptions, query
from dotenv import load_dotenv
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler
from slack_bolt.async_app import AsyncApp

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
log = logging.getLogger("cos-slack-bot")

# --- Config --------------------------------------------------------------

SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]
ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
CLAUDE_PROJECT_DIR = Path(
    os.environ.get("CLAUDE_PROJECT_DIR", Path(__file__).resolve().parent.parent)
)
CLAUDE_MODEL = os.environ.get("CLAUDE_MODEL", "claude-opus-4-6")

ALLOWED_USER_IDS = {
    uid.strip()
    for uid in os.environ.get("ALLOWED_SLACK_USER_IDS", "").split(",")
    if uid.strip()
}

if not ALLOWED_USER_IDS:
    log.warning(
        "ALLOWED_SLACK_USER_IDS is empty — NO users will be able to use the bot. "
        "Set this env var to a comma-separated list of Slack user IDs."
    )

# Ensure the Agent SDK picks up the API key.
os.environ["ANTHROPIC_API_KEY"] = ANTHROPIC_API_KEY

# --- Slack app -----------------------------------------------------------

app = AsyncApp(token=SLACK_BOT_TOKEN)

SYSTEM_PROMPT = """You are the user's AI Chief of Staff, accessed via Slack.

You have a full suite of specialized skills available in .claude/skills/ and
MCP integrations for Google Workspace, Microsoft 365, Jira, and Trello.

Slack rendering rules:
- Use Slack mrkdwn (NOT standard markdown).
  - Bold: *text*  (single asterisks)
  - Italic: _text_
  - Code: `inline` or ```block```
  - Lists: leading "- " or "1. "
- Keep responses concise. Slack is a chat interface, not a document.
- For long outputs (reports, tables), offer to save to a file instead.
- Always surface the most important info first.
"""


def is_authorized(user_id: str) -> bool:
    """Return True if the Slack user is on the allowlist."""
    return user_id in ALLOWED_USER_IDS


async def ask_claude(prompt: str) -> str:
    """Send a prompt to Claude via the Agent SDK and return the full response."""
    options = ClaudeAgentOptions(
        model=CLAUDE_MODEL,
        system_prompt=SYSTEM_PROMPT,
        cwd=str(CLAUDE_PROJECT_DIR),
        # Pick up .claude/skills/ and .mcp.json from the project directory.
        setting_sources=["project"],
        permission_mode="default",
    )

    chunks: list[str] = []
    async for message in query(prompt=prompt, options=options):
        # The SDK yields assistant messages with content blocks. Collect text.
        content = getattr(message, "content", None)
        if content is None:
            continue
        for block in content:
            text = getattr(block, "text", None)
            if text:
                chunks.append(text)

    return "".join(chunks).strip() or "_(no response)_"


async def handle_user_message(event: dict, say) -> None:
    """Shared handler for both DMs and @mentions."""
    user_id = event.get("user")
    text = (event.get("text") or "").strip()
    thread_ts = event.get("thread_ts") or event.get("ts")

    if not user_id or not text:
        return

    if not is_authorized(user_id):
        log.warning("Rejected message from unauthorized user %s", user_id)
        await say(
            text=(
                "Sorry, you're not authorized to use this bot. "
                "Ask the admin to add your user ID to `ALLOWED_SLACK_USER_IDS`."
            ),
            thread_ts=thread_ts,
        )
        return

    # Strip the bot mention if present.
    if text.startswith("<@"):
        text = text.split(">", 1)[-1].strip()

    log.info("Query from %s: %s", user_id, text[:120])

    # Send an immediate ack so the user knows we're working.
    ack = await say(text="_thinking..._", thread_ts=thread_ts)
    ack_ts = ack.get("ts")

    try:
        response = await ask_claude(text)
    except Exception as exc:
        log.exception("Claude query failed")
        response = f":warning: Error: `{exc}`"

    # Replace the "thinking..." message with the real response.
    # Slack messages have a 40k char limit; chunk if longer.
    MAX = 3800
    if len(response) <= MAX:
        await app.client.chat_update(
            channel=event["channel"], ts=ack_ts, text=response
        )
    else:
        await app.client.chat_update(
            channel=event["channel"], ts=ack_ts, text=response[:MAX]
        )
        for i in range(MAX, len(response), MAX):
            await say(text=response[i : i + MAX], thread_ts=thread_ts)


@app.event("message")
async def on_direct_message(event, say):
    """Handle DMs to the bot."""
    # Ignore messages from bots (including our own) and edits/deletes.
    if event.get("bot_id") or event.get("subtype"):
        return
    # Only handle DM channels (channel_type == "im").
    if event.get("channel_type") != "im":
        return
    await handle_user_message(event, say)


@app.event("app_mention")
async def on_mention(event, say):
    """Handle @-mentions of the bot in channels."""
    await handle_user_message(event, say)


async def main() -> None:
    log.info("Starting Chief of Staff Slack bot")
    log.info("Project dir: %s", CLAUDE_PROJECT_DIR)
    log.info("Model: %s", CLAUDE_MODEL)
    log.info("Allowed users: %d", len(ALLOWED_USER_IDS))
    handler = AsyncSocketModeHandler(app, SLACK_APP_TOKEN)
    await handler.start_async()


if __name__ == "__main__":
    asyncio.run(main())
