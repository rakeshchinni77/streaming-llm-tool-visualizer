import useChatStore from "../store/chatStore";
import streamClient from "../services/streamClient";

export default function useChat() {
  const addMessage = useChatStore((s) => s.addMessage);
  const appendAssistantDelta = useChatStore((s) => s.appendAssistantDelta);
  const addToolCall = useChatStore((s) => s.addToolCall);
  const updateToolCall = useChatStore((s) => s.updateToolCall);
  const setTokenCount = useChatStore((s) => s.setTokenCount);
  const setStreamingStatus = useChatStore((s) => s.setStreamingStatus);

  async function sendMessage(userText) {
    if (!userText || !userText.trim()) return;

    // Add user message immediately
    const userMessage = { id: String(Date.now()) + "-u", role: "user", content: userText };
    addMessage(userMessage);

    // Add empty assistant message to be filled
    const assistantMessage = { id: String(Date.now()) + "-a", role: "assistant", content: "" };
    addMessage(assistantMessage);

    setStreamingStatus("streaming");

    const messages = [
      { role: "user", content: userText },
    ];

    const abort = await streamClient.streamChat(
      messages,
      (delta) => {
        appendAssistantDelta(delta);
      },
      (payload) => {
        if (payload && typeof payload.totalTokens === "number") {
          setTokenCount(payload.totalTokens);
        }
        setStreamingStatus("idle");
      },
      (err) => {
        console.error("Streaming error:", err);
        setStreamingStatus("idle");
        appendAssistantDelta("\nUnable to connect to server.");
      },
      (payload) => {
        if (!payload || !payload.id) return;
        const toolMessage = {
          id: `tool-${payload.id}`,
          type: "tool_call",
          role: "assistant",
          tool: payload.tool,
          status: "Running",
          input: payload.input,
          result: null,
          error: null,
        };
        addToolCall(toolMessage);
      },
      (payload) => {
        if (!payload || !payload.id) return;
        if (payload.result) {
          updateToolCall(payload.id, {
            status: "Completed",
            result: payload.result,
            error: null,
          });
        } else if (payload.error) {
          updateToolCall(payload.id, {
            status: "Failed",
            error: payload.error,
          });
        }
      }
    );

    return abort;
  }

  return { sendMessage };
}
