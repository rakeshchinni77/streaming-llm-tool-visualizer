export async function streamChat(
  messages,
  onDelta,
  onDone,
  onError,
  onToolCallStart,
  onToolResult
) {
  const controller = new AbortController();
  const signal = controller.signal;
  let doneEventReceived = false;

  function handleEvent(event, payload) {
    if (!payload) return;

    if (event === "text_delta" && typeof payload.delta === "string") {
      onDelta && onDelta(payload.delta);
    } else if (event === "tool_call_start") {
      onToolCallStart && onToolCallStart(payload);
    } else if (event === "tool_result") {
      onToolResult && onToolResult(payload);
    } else if (event === "done") {
      doneEventReceived = true;
      onDone && onDone(payload);
    } else if (event === "error") {
      onError && onError(new Error(payload.message || "An error occurred during streaming."));
      controller.abort();
    }
  }

  function parseSseChunk(part) {
    const lines = part.split(/\r?\n/).map((l) => l.trim());
    let event = null;
    const dataLines = [];

    for (const line of lines) {
      if (line.startsWith("event:")) {
        event = line.slice(6).trim();
      } else if (line.startsWith("data:")) {
        dataLines.push(line.slice(5).trim());
      }
    }

    if (event && dataLines.length > 0) {
      const dataStr = dataLines.join("\n");
      try {
        const payload = JSON.parse(dataStr);
        handleEvent(event, payload);
      } catch (e) {
        console.error("Failed to parse SSE data", dataStr, e);
      }
    }
  }

  try {
    const resp = await fetch("http://localhost:8000/api/chat/stream", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ messages }),
      signal,
    });

    if (!resp.ok) {
      const text = await resp.text();
      throw new Error(`Stream request failed: ${resp.status} ${text}`);
    }

    const reader = resp.body.getReader();
    const decoder = new TextDecoder("utf-8");
    let buffer = "";

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });

      let parts = buffer.split(/\r?\n\r?\n/);
      buffer = parts.pop();

      for (const part of parts) {
        parseSseChunk(part);
      }
    }

    if (buffer.trim()) {
      parseSseChunk(buffer);
    }

    if (!doneEventReceived) {
      onDone && onDone();
    }
  } catch (err) {
    onError && onError(err);
  }

  return () => controller.abort();
}

export default { streamChat };
