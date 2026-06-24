import React from "react";

export default function ContextMonitor() {
  return (
    <section className="card context-monitor" data-testid="context-monitor">
      <div>
        <div className="label">Context</div>
        <div className="token-count" data-testid="total-tokens">
          Tokens: 0
        </div>
      </div>

      <button type="button" data-testid="compress-button" disabled>
        Compress Conversation
      </button>
    </section>
  );
}

