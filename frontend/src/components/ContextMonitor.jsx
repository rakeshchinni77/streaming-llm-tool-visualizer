import React from "react";
import useChatStore from "../store/chatStore";

export default function ContextMonitor() {
  const tokenCount = useChatStore((state) => state.tokenCount);

  return (
    <section className="card context-monitor" data-testid="context-monitor">
      <div>
        <div className="label">Context</div>
        <div className="token-count" data-testid="total-tokens">
          Tokens: {tokenCount}
        </div>
      </div>

      <button type="button" data-testid="compress-button" disabled>
        Compress Conversation
      </button>
    </section>
  );
}

