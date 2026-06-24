export async function streamChat(messages, onDelta, onDone, onError) {
  const controller = new AbortController();
  const signal = controller.signal;

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

      // Split on double newline which delimits SSE events
      let parts = buffer.split(/\r?\n\r?\n/);
      buffer = parts.pop(); // remainder

      for (const part of parts) {
        // Each part may contain lines like 'event: text_delta' and 'data: {...}'
        const lines = part.split(/\r?\n/).map((l) => l.trim());
        let event = null;
        let dataLines = [];
        for (const line of lines) {
          if (line.startsWith("event:")) {
            event = line.slice(6).trim();
          } else if (line.startsWith("data:")) {
            dataLines.push(line.slice(5).trim());
          }
        }

        if (dataLines.length > 0) {
          const dataStr = dataLines.join("\n");
          try {
            const payload = JSON.parse(dataStr);
            if (event === "text_delta" && payload && typeof payload.delta === "string") {
              onDelta(payload.delta);
            }
          } catch (e) {
            // ignore malformed JSON but notify
            console.error("Failed to parse SSE data", dataStr, e);
          }
        }
      }
    }

    // If there's remaining buffer, try to parse it as one final event
    if (buffer.trim()) {
      const lines = buffer.split(/\r?\n/).map((l) => l.trim());
      let event = null;
      let dataLines = [];
      for (const line of lines) {
        if (line.startsWith("event:")) {
          event = line.slice(6).trim();
        } else if (line.startsWith("data:")) {
          dataLines.push(line.slice(5).trim());
        }
      }
      if (dataLines.length > 0) {
        try {
          const payload = JSON.parse(dataLines.join("\n"));
          if (event === "text_delta" && payload && typeof payload.delta === "string") {
            onDelta(payload.delta);
          }
        } catch (e) {
          console.error("Failed to parse final SSE data", dataLines.join("\n"), e);
        }
      }
    }

    onDone && onDone();
  } catch (err) {
    onError && onError(err);
  }

  return () => controller.abort();
}

export default { streamChat };
