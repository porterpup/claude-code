# Phone Agent MCP Server

An MCP server that enables Claude Code to make AI-powered outbound phone calls via [Bland.ai](https://www.bland.ai/) for scheduling appointments, making reservations, and other phone tasks.

## How it works

1. You tell Claude: *"Call my dentist at 555-123-4567 and schedule a cleaning next week"*
2. Claude formulates the objective and context
3. The MCP server triggers a Bland.ai API call
4. An AI voice agent makes the actual phone call
5. The AI identifies itself as an AI assistant calling on your behalf
6. The call result (transcript, summary, outcome) is returned to Claude
7. Claude reports the result to you

## Setup

### 1. Get a Bland.ai API key

1. Sign up at https://www.bland.ai/
2. Get your API key from the dashboard
3. Add credits (pay-as-you-go, ~$0.09/minute)

### 2. Install

```bash
cd mcp-phone-agent
npm install
```

### 3. Configure in Claude Code

Already added to `.mcp.json`. Just fill in your env vars:

```json
"phone-agent": {
  "command": "node",
  "args": ["mcp-phone-agent/src/index.js"],
  "env": {
    "BLAND_API_KEY": "sk-your-bland-api-key",
    "CALLER_NAME": "Your Name"
  }
}
```

## Tools exposed

### `make_phone_call`
Make an outbound call with a natural language objective.

**Parameters:**
- `phone_number` (required) — Phone number to call
- `objective` (required) — What the call should accomplish
- `talking_points` (optional) — Context for the AI (your name, DOB, preferences)
- `max_duration_minutes` (optional, default: 5) — Max call length
- `wait_for_completion` (optional, default: true) — Wait for call to finish

**Returns:** Status, transcript, summary, duration

### `get_call_status`
Check on a previously initiated call.

**Parameters:**
- `call_id` — From a previous `make_phone_call`

## Cost

- ~$0.09/minute with Bland.ai
- 5-10 calls/month at ~2-3 min each = **$1-3/month**
- No monthly subscription

## Important notes

- The AI **always identifies itself as AI** at the start of every call
- Recording is **disabled by default** to avoid two-party consent issues
- This is for personal use — scheduling appointments, reservations, etc.
- Don't use for spam, marketing, or harassment
- Review Bland.ai's terms of service
