"""Chief of Staff Slack Bot.

A Slack bot that bridges Slack messages to the Claude Agent SDK, giving you
chat access to your full Chief of Staff skill suite and MCP integrations.

Architecture:
    Slack (Socket Mode) -> Slack Bolt handler -> Claude Agent SDK -> Claude
                                                      |
                                                      v
                                        .claude/skills/ + .mcp.json
                                        (Gmail, MS365, Jira, Trello, ...)

Features:
- Socket Mode (no public URL required)
- Slack user ID allowlist for access control
- Session persistence: each Slack thread resumes its Claude session
- Reaction indicators (:eyes: while working, :white_check_mark: on done)
- Chunks responses over Slack's 40k character limit
- Inherits Chief of Staff system prompt via "claude_code" preset + skills
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

from sessions import SessionStore

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
SESSION_DB = Path(
    os.environ.get("SESSION_DB", Path(__file__).resolve().parent / "data" / "sessions.db")
)

ALLOWED_USER_IDS = {
    uid.strip()
    for uid in os.environ.get("ALLOWED_SLACK_USER_IDS", "").split(",")
    if uid.strip()
}

if not ALLOWED_USER_IDS:
    log.warning(
        "ALLOWED_SLACK_USER_IDS is empty - NO users will be able to use the bot. "
        "Set this env var to a comma-separated list of Slack user IDs."
    )

# Ensure the Agent SDK picks up the API key.
os.environ["ANTHROPIC_API_KEY"] = ANTHROPIC_API_KEY

# --- Slack + session store -----------------------------------------------

app = AsyncApp(token=SLACK_BOT_TOKEN)
sessions = SessionStore(SESSION_DB)

# Additional guidance appended to Claude Code's built-in preset system prompt.
# The preset already knows about skills (including chief-of-staff orchestrator).
SLACK_APPEND = """
You are being accessed from Slack. Apply these rendering rules:

- Use Slack mrkdwn, NOT standard markdown:
  - Bold: *text* (single asterisks)
  - Italic: _text_
  - Code: `inline` or triple-backtick blocks
  - Lists: leading "- " or "1. "
  - Links: <https://example.com|link text>
- Keep responses concise - Slack is a chat interface, not a document.
- For long deliverables (reports, tables), save to a file and link to it instead of pasting.
- Surface the most important information first.
- When invoking the Chief of Staff skill suite, delegate to specialized skills
  (meeting-notes, email-draft, briefing, etc.) as appropriate.
"""


def is_authorized(user_id: str) -> bool:
    """Return True if the Slack user is on the allowlist."""
    return user_id in ALLOWED_USER_IDS


def _extract_text(message) -> str:
    """Pull plain text out of an Agent SDK message (assistant or result)."""
    content = getattr(message, "content", None)
    if content is None:
        # ResultMessage exposes .result directly.
        return getattr(message, "result", "") or ""
    parts: list[str] = []
    for block in content:
        text = getattr(block, "text", None)
        if text:
            parts.append(text)
    return "".join(parts)


async def ask_claude(
    prompt: str, resume_session_id: str | None
) -> tuple[str, str | None]:
    """Send a prompt to Claude and return (response_text, new_session_id)."""
    options = ClaudeAgentOptions(
        model=CLAUDE_MODEL,
        # Use Claude Code's built-in preset so skills are discovered/invoked
        # properly. Append our Slack-specific guidance on top.
        system_prompt={
            "type": "preset",
            "preset": "claude_code",
            "append": SLACK_APPEND,
        },
        cwd=str(CLAUDE_PROJECT_DIR),
        # Pick up .claude/skills/ and .mcp.json from the project directory.
        setting_sources=["project"],
        permission_mode="default",
        resume=resume_session_id,
        max_turns=30,
    )

    chunks: list[str] = []
    new_session_id: str | None = None

    async for message in query(prompt=prompt, options=options):
        # Capture session id from the init system message for later resume.
        if (
            getattr(message, "subtype", None) == "init"
            and isinstance(getattr(message, "data", None), dict)
        ):
            sid = message.data.get("session_id")
            if sid:
                new_session_id = sid

        chunks.append(_extract_text(message))

    return "".join(chunks).strip() or "_(no response)_", new_session_id


async def handle_user_message(event: dict, say, client) -> None:
    """Shared handler for both DMs and @mentions."""
    user_id = event.get("user")
    text = (event.get("text") or "").strip()
    channel = event["channel"]
    # Thread continuity: use existing thread_ts if this is a reply,
    # otherwise use this message's ts as the root of a new thread.
    thread_ts = event.get("thread_ts") or event.get("ts")
    msg_ts = event.get("ts")

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

    log.info("Query from %s (thread %s): %s", user_id, thread_ts, text[:120])

    # Visual status indicator on the user's message.
    try:
        await client.reactions_add(channel=channel, timestamp=msg_ts, name="eyes")
    except Exception:
        pass  # reactions_add fails if already added or missing scope; not fatal.

    # Post a placeholder we'll edit with the real response.
    ack = await say(text="_thinking..._", thread_ts=thread_ts)
    ack_ts = ack.get("ts")

    # Look up any existing Claude session for this Slack thread.
    prior_session = sessions.get(thread_ts)
    if prior_session:
        log.info("Resuming Claude session %s for thread %s", prior_session, thread_ts)

    try:
        response, new_session_id = await ask_claude(text, prior_session)
        if new_session_id:
            sessions.set(thread_ts, new_session_id)
    except Exception as exc:
        log.exception("Claude query failed")
        response = f":warning: Error: `{exc}`"
        new_session_id = None

    # Replace the "thinking..." message with the real response.
    # Slack messages have a 40k char limit; chunk if longer.
    MAX = 3800
    if len(response) <= MAX:
        await client.chat_update(channel=channel, ts=ack_ts, text=response)
    else:
        await client.chat_update(channel=channel, ts=ack_ts, text=response[:MAX])
        for i in range(MAX, len(response), MAX):
            await say(text=response[i : i + MAX], thread_ts=thread_ts)

    # Swap :eyes: -> :white_check_mark: to signal done.
    try:
        await client.reactions_remove(channel=channel, timestamp=msg_ts, name="eyes")
    except Exception:
        pass
    try:
        await client.reactions_add(
            channel=channel, timestamp=msg_ts, name="white_check_mark"
        )
    except Exception:
        pass


@app.event("message")
async def on_direct_message(event, say, client):
    """Handle DMs to the bot."""
    # Ignore messages from bots (including our own) and edits/deletes.
    if event.get("bot_id") or event.get("subtype"):
        return
    # Only handle DM channels (channel_type == "im").
    if event.get("channel_type") != "im":
        return
    await handle_user_message(event, say, client)


@app.event("app_mention")
async def on_mention(event, say, client):
    """Handle @-mentions of the bot in channels."""
    await handle_user_message(event, say, client)


async def main() -> None:
    log.info("Starting Chief of Staff Slack bot")
    log.info("Project dir: %s", CLAUDE_PROJECT_DIR)
    log.info("Model: %s", CLAUDE_MODEL)
    log.info("Session db: %s", SESSION_DB)
    log.info("Allowed users: %d", len(ALLOWED_USER_IDS))

    # Periodic cleanup of stale sessions.
    async def cleanup_loop():
        while True:
            await asyncio.sleep(3600)
            removed = sessions.cleanup_stale()
            if removed:
                log.info("Cleaned up %d stale sessions", removed)

    asyncio.create_task(cleanup_loop())

    handler = AsyncSocketModeHandler(app, SLACK_APP_TOKEN)
    await handler.start_async()


if __name__ == "__main__":
    asyncio.run(main())
