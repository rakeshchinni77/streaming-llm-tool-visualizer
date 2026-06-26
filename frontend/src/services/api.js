export async function summarizeConversation(messages) {
  const response = await fetch("http://localhost:8000/api/chat/summarize", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ messages }),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Summarization failed: ${errorText}`);
  }

  return response.json();
}
