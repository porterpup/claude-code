---
name: phone-call
description: Make AI-powered phone calls to schedule appointments, make reservations, or handle phone tasks. The AI identifies itself and acts on your behalf.
allowed-tools: Read Grep Glob Bash Write Edit TodoWrite
argument-hint: ["call [number] to [objective]", "schedule appointment at [place]", "make reservation at [restaurant]"]
---

# Phone Call Agent

You can make outbound phone calls on the user's behalf using the `phone-agent` MCP
server (Bland.ai). The AI voice agent will identify itself as an AI assistant,
conduct the conversation, and return the result.

## When to Use

- Scheduling appointments (dentist, doctor, haircut, auto shop, etc.)
- Making restaurant reservations
- Calling businesses to check hours, availability, or pricing
- Following up on orders, deliveries, or service requests
- Any phone call the user doesn't want to make themselves

## Process

### 1. Gather Information

Before making a call, ensure you have:

| Required | Details |
|----------|---------|
| **Phone number** | In any format — you'll normalize to E.164 |
| **Objective** | What the call should accomplish |
| **User's name** | For the AI to use on the call |

| Optional but helpful | Details |
|---------------------|---------|
| **Preferred dates/times** | For appointment scheduling |
| **Constraints** | "Only mornings", "Not Fridays", "Before June 1" |
| **Personal info needed** | DOB, insurance, account number (only if required) |
| **Fallback options** | "If Tuesday is full, try Wednesday" |

### 2. Confirm Before Calling

**ALWAYS confirm with the user before initiating a call.** Present:

> I'll call **[business name]** at **[phone number]** to:
> - **Objective:** [what the call will do]
> - **Context I'll provide:** [talking points]
> - **Your name:** [name]
> - **Max duration:** [X] minutes
>
> Shall I make this call?

Only proceed after explicit user approval.

### 3. Make the Call

Use the `make_phone_call` MCP tool:
- `phone_number`: The number to call
- `objective`: Clear, specific natural language objective
- `talking_points`: Array of context strings
- `max_duration_minutes`: Default 5, increase for complex calls
- `wait_for_completion`: true (wait for result)

### 4. Report Results

After the call, present a structured summary:

#### Call Result: [Business Name]

| Field | Details |
|-------|---------|
| **Status** | Completed / Failed / Voicemail |
| **Duration** | X min Y sec |
| **Outcome** | [What was accomplished] |

**Key Details:**
- [Appointment date/time if scheduled]
- [Confirmation number if given]
- [Any follow-up required]
- [Important info mentioned by the other party]

**Full Transcript:** [Available if needed]

### 5. Follow Up

After a successful call:
- Offer to add the appointment to their calendar (via calendar MCP)
- Log the outcome in memory (`/memory`)
- Create a reminder if follow-up is needed

## Safety Rules

1. **Always confirm before calling.** Never auto-dial.
2. **AI identifies itself.** Every call starts with "Hi, I'm an AI assistant calling on behalf of [name]."
3. **No sensitive data in objectives.** Don't include SSN, full credit card numbers, or passwords in the call task. Share only what's needed (last 4 digits, DOB, etc.).
4. **Recording is disabled.** Two-party consent states require all parties to agree to recording.
5. **Max 5-minute default.** Extend only if the user requests or the task clearly requires it.
6. **Personal use only.** Not for marketing, solicitation, or bulk calling.

## Input

$ARGUMENTS
