#!/usr/bin/env python3
"""Generic bot runner for a Slack agent in the #cos swarm.

Ephemeral invocation model: holds a Socket Mode websocket per agent,
spawns a fresh `claude -p` subprocess on each @mention, posts the
response back in-thread.

Usage:
    AGENT=cos         python3 runner.py
    AGENT=cos-notion  python3 runner.py

Tokens are loaded from ./.env.slack (not committed).
"""
from __future__ import annotations

import logging
import os
import re
import subprocess
import sys
import threading
import time
from pathlib import Path

from slack_sdk import WebClient
from slack_sdk.socket_mode import SocketModeClient
from slack_sdk.socket_mode.request import SocketModeRequest
from slack_sdk.socket_mode.response import SocketModeResponse

sys.path.insert(0, str(Path(__file__).parent))
from agents import AGENTS  # noqa: E402

AGENT = os.environ.get("AGENT")
if not AGENT or AGENT not in AGENTS:
    print(f"Set AGENT to one of: {list(AGENTS)}", file=sys.stderr)
    sys.exit(1)

# Load .env.slack ourselves (no python-dotenv dep).
env_path = Path(__file__).parent / ".env.slack"
if env_path.exists():
    for line in env_path.read_text().splitlines():
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

UPPER = AGENT.upper().replace("-", "_")
BOT_TOKEN = os.environ[f"{UPPER}_BOT_TOKEN"]
APP_TOKEN = os.environ[f"{UPPER}_APP_TOKEN"]

CONFIG = AGENTS[AGENT]
REPO_ROOT = Path("/home/user/claude-code")

logging.basicConfig(
    level=logging.INFO,
    format=f"[%(asctime)s {AGENT}] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(AGENT)

web = WebClient(token=BOT_TOKEN)
auth = web.auth_test()
MY_USER_ID: str = auth["user_id"]
MY_BOT_ID: str = auth.get("bot_id") or ""
log.info(f"Auth OK — user_id={MY_USER_ID} bot_id={MY_BOT_ID} handle={auth['user']}")

# Per-agent other-agent IDs — look up at startup so system prompts can be
# dynamically substituted (@cos delegates to @cos-notion by their numeric ID).
OTHER_AGENT_IDS: dict[str, str] = {}
for other in AGENTS:
    if other == AGENT:
        continue
    other_upper = other.upper().replace("-", "_")
    other_token = os.environ.get(f"{other_upper}_BOT_TOKEN")
    if not other_token:
        continue
    try:
        other_auth = WebClient(token=other_token).auth_test()
        OTHER_AGENT_IDS[other] = other_auth["user_id"]
        log.info(f"Discovered @{other} = {other_auth['user_id']}")
    except Exception as e:
        log.warning(f"Couldn't resolve @{other}: {e}")


def is_addressed_to_me(text: str) -> bool:
    return f"<@{MY_USER_ID}>" in (text or "")


def should_process(event: dict) -> bool:
    if event.get("subtype") in {"message_changed", "message_deleted"}:
        return False
    # Ignore own messages.
    if event.get("user") == MY_USER_ID:
        return False
    if event.get("bot_id") and event.get("bot_id") == MY_BOT_ID:
        return False
    # Only respond if we're @-mentioned.
    return is_addressed_to_me(event.get("text", ""))


def strip_mention(text: str) -> str:
    return re.sub(rf"<@{MY_USER_ID}>\s*", "", text or "").strip()


def build_system_prompt() -> str:
    prompt = CONFIG["system_prompt"]
    # Substitute <@COS_NOTION_USER_ID> style placeholders with real IDs.
    for other, uid in OTHER_AGENT_IDS.items():
        placeholder = f"<@{other.upper().replace('-', '_')}_USER_ID>"
        prompt = prompt.replace(placeholder, f"<@{uid}>")
    return prompt


SYSTEM_PROMPT = build_system_prompt()


# Per-agent settings JSON with permissions.allow list. Claude's
# --permission-mode bypassPermissions can't be used inside this sandbox
# (it maps to --dangerously-skip-permissions which is blocked for root).
# Instead we whitelist specific tools via the settings file so they
# auto-approve without prompting.
SETTINGS_FILES = {
    "cos":        str(Path(__file__).parent / "agent-settings-cos.json"),
    "cos-notion": str(Path(__file__).parent / "agent-settings-notion.json"),
    "cos-inbox":  str(Path(__file__).parent / "agent-settings-inbox.json"),
}


# Serialize claude -p calls: each subprocess spins up MCP servers that
# use ~10GB RSS. Concurrent calls OOM the sandbox.
_claude_lock = threading.Lock()


def call_claude(user_text: str) -> str:
    """Invoke `claude -p` with agent persona; return stdout."""
    if not _claude_lock.acquire(timeout=0):
        return "_(busy — another request is in progress, try again in a minute)_"
    try:
        settings = SETTINGS_FILES.get(AGENT, SETTINGS_FILES["cos"])
        cmd = [
            "claude",
            "-p",
            user_text,
            "--append-system-prompt", SYSTEM_PROMPT,
            "--settings", settings,
            "--output-format", "text",
        ]
        log.info(f"invoking claude (prompt={user_text[:120]!r})")
        start = time.time()
        timeout = 600 if AGENT == "cos-inbox" else 180
        env = os.environ.copy()
        env["GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE"] = "/tmp/gws-creds.json"
        try:
            result = subprocess.run(
                cmd,
                cwd=str(REPO_ROOT),
                capture_output=True,
                text=True,
                timeout=timeout,
                env=env,
            )
        except subprocess.TimeoutExpired:
            return "_(Claude call timed out.)_"
        dt = time.time() - start
        log.info(f"claude returned in {dt:.1f}s, rc={result.returncode}")
        if result.returncode != 0:
            return f"_(Claude errored rc={result.returncode}: {result.stderr[:400]})_"
        return (result.stdout or "").strip() or "_(Claude returned empty output.)_"
    finally:
        _claude_lock.release()


def handle_event(client: SocketModeClient, req: SocketModeRequest) -> None:
    # Always ack promptly so Slack doesn't retry.
    client.send_socket_mode_response(SocketModeResponse(envelope_id=req.envelope_id))

    if req.type != "events_api":
        return
    event = req.payload.get("event", {})
    # Only handle `message` events. Slack fires BOTH `app_mention` AND
    # `message.channels` for the same @-mention; handling only `message`
    # dedupes naturally while still covering DMs (message.im) and channel
    # posts (message.channels / message.groups).
    if event.get("type") != "message":
        return
    if not should_process(event):
        return

    user_text = strip_mention(event.get("text", ""))
    channel = event.get("channel")
    thread_ts = event.get("thread_ts") or event.get("ts")
    log.info(f"processing message in {channel} thread={thread_ts}: {user_text[:120]!r}")

    try:
        reply = call_claude(user_text)
    except Exception as e:
        log.exception("Claude call blew up")
        reply = f"_(internal error: {e})_"

    try:
        web.chat_postMessage(channel=channel, text=reply, thread_ts=thread_ts)
    except Exception as e:
        log.exception(f"chat.postMessage failed: {e}")


def main() -> None:
    sm = SocketModeClient(app_token=APP_TOKEN, web_client=web)
    sm.socket_mode_request_listeners.append(handle_event)
    sm.connect()
    log.info("Socket Mode connected. Listening.")
    # Block forever.
    while True:
        time.sleep(3600)


if __name__ == "__main__":
    main()
