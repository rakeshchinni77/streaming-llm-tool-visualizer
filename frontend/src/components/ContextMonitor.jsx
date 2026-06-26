import React from "react";
import useChatStore from "../store/chatStore";
import { summarizeConversation } from "../services/api";

export default function ContextMonitor() {
  const tokenCount = useChatStore((state) => state.tokenCount);
  const messages = useChatStore((state) => state.messages);
  const setMessages = useChatStore((state) => state.setMessages);

  const handleCompress = async () => {
    try {
      const { summary } = await summarizeConversation(messages);
      setMessages([
        { id: String(Date.now()) + "-system", role: "system", content: "Conversation Summary" },
        { id: String(Date.now()) + "-assistant", role: "assistant", content: summary },
      ]);
    } catch (err) {
      console.error("Summarization failed:", err);
      alert("Summarization failed. Please try again.");
    }
  };

  return (
    <section className="card context-monitor" data-testid="context-monitor">
      <div>
        <div className="label">Context</div>
        <div className="token-count" data-testid="total-tokens">
          Tokens: {tokenCount}
        </div>
      </div>

      <button type="button" data-testid="compress-button" onClick={handleCompress}>
        Compress Conversation
      </button>
    </section>
  );
}

