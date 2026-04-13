import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const BLAND_API_KEY = process.env.BLAND_API_KEY;
const CALLER_NAME = process.env.CALLER_NAME || "the user";
const BLAND_API_URL = "https://api.bland.ai/v1";

if (!BLAND_API_KEY) {
  console.error("BLAND_API_KEY environment variable is required");
  process.exit(1);
}

async function blandPost(path, body) {
  const res = await fetch(`${BLAND_API_URL}${path}`, {
    method: "POST",
    headers: {
      Authorization: BLAND_API_KEY,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Bland API error ${res.status}: ${text}`);
  }
  return res.json();
}

async function blandGet(path) {
  const res = await fetch(`${BLAND_API_URL}${path}`, {
    headers: { Authorization: BLAND_API_KEY },
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Bland API error ${res.status}: ${text}`);
  }
  return res.json();
}

async function pollCallCompletion(callId, maxWaitMs = 300000) {
  const pollInterval = 5000;
  const deadline = Date.now() + maxWaitMs;

  while (Date.now() < deadline) {
    const data = await blandGet(`/calls/${callId}`);
    const status = data.status || data.call_status;

    if (status === "completed" || status === "ended") {
      return data;
    }
    if (status === "failed" || status === "error") {
      return data;
    }

    await new Promise((r) => setTimeout(r, pollInterval));
  }

  return { status: "timeout", message: "Call did not complete within 5 minutes" };
}

// --- MCP Server ---

const server = new McpServer({
  name: "phone-agent",
  version: "1.0.0",
});

server.tool(
  "make_phone_call",
  "Make an AI-powered outbound phone call to schedule appointments, make reservations, or handle other phone tasks. The AI will identify itself as an AI assistant at the start of the call.",
  {
    phone_number: z
      .string()
      .describe(
        'Phone number to call in E.164 format (e.g., "+15551234567") or standard format (e.g., "555-123-4567")'
      ),
    objective: z
      .string()
      .describe(
        'What the call should accomplish, in natural language (e.g., "Schedule a dental cleaning for next Tuesday morning")'
      ),
    talking_points: z
      .array(z.string())
      .optional()
      .describe(
        "Additional context the AI should know during the call (your name, date of birth, preferences, constraints, etc.)"
      ),
    max_duration_minutes: z
      .number()
      .optional()
      .default(5)
      .describe("Maximum call duration in minutes (default: 5)"),
    wait_for_completion: z
      .boolean()
      .optional()
      .default(true)
      .describe(
        "If true, waits for the call to complete and returns the result. If false, returns immediately with a call_id for later polling."
      ),
  },
  async ({
    phone_number,
    objective,
    talking_points,
    max_duration_minutes,
    wait_for_completion,
  }) => {
    const context = talking_points?.length
      ? `\n\nAdditional context:\n${talking_points.map((t) => `- ${t}`).join("\n")}`
      : "";

    const task = `${objective}${context}`;

    const callPayload = {
      phone_number,
      task,
      first_sentence: `Hi, I'm an AI assistant calling on behalf of ${CALLER_NAME}.`,
      voice: "nat",
      max_duration: max_duration_minutes,
      wait_for_greeting: true,
      record: false,
    };

    try {
      const callResult = await blandPost("/calls", callPayload);
      const callId = callResult.call_id;

      if (!callId) {
        return {
          content: [
            {
              type: "text",
              text: `Failed to initiate call: ${JSON.stringify(callResult)}`,
            },
          ],
        };
      }

      if (!wait_for_completion) {
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify(
                {
                  status: "initiated",
                  call_id: callId,
                  message: `Call initiated to ${phone_number}. Use get_call_status with call_id "${callId}" to check the result.`,
                },
                null,
                2
              ),
            },
          ],
        };
      }

      // Poll until the call completes.
      const result = await pollCallCompletion(callId);
      const status = result.status || result.call_status || "unknown";
      const transcript = result.transcripts || result.transcript || [];
      const summary = result.summary || result.analysis || "";

      const output = {
        status,
        call_id: callId,
        phone_number,
        duration_seconds: result.call_length || result.duration || null,
        summary: typeof summary === "string" ? summary : JSON.stringify(summary),
        transcript:
          typeof transcript === "string"
            ? transcript
            : Array.isArray(transcript)
              ? transcript
                  .map((t) => `${t.speaker || t.role || "?"}: ${t.text || t.content || ""}`)
                  .join("\n")
              : JSON.stringify(transcript),
      };

      return {
        content: [{ type: "text", text: JSON.stringify(output, null, 2) }],
      };
    } catch (err) {
      return {
        content: [
          {
            type: "text",
            text: `Error making phone call: ${err.message}`,
          },
        ],
        isError: true,
      };
    }
  }
);

server.tool(
  "get_call_status",
  "Check the status and result of a previously initiated phone call.",
  {
    call_id: z.string().describe("The call_id returned from make_phone_call"),
  },
  async ({ call_id }) => {
    try {
      const result = await blandGet(`/calls/${call_id}`);
      const status = result.status || result.call_status || "unknown";
      const transcript = result.transcripts || result.transcript || [];
      const summary = result.summary || result.analysis || "";

      const output = {
        status,
        call_id,
        duration_seconds: result.call_length || result.duration || null,
        summary: typeof summary === "string" ? summary : JSON.stringify(summary),
        transcript:
          typeof transcript === "string"
            ? transcript
            : Array.isArray(transcript)
              ? transcript
                  .map((t) => `${t.speaker || t.role || "?"}: ${t.text || t.content || ""}`)
                  .join("\n")
              : JSON.stringify(transcript),
      };

      return {
        content: [{ type: "text", text: JSON.stringify(output, null, 2) }],
      };
    } catch (err) {
      return {
        content: [
          { type: "text", text: `Error checking call status: ${err.message}` },
        ],
        isError: true,
      };
    }
  }
);

// --- Start ---

const transport = new StdioServerTransport();
await server.connect(transport);
