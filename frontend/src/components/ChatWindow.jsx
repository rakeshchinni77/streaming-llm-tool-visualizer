import React from "react";

export default function ChatWindow() {
  return (
    <section
      className="card chat-window"
      data-testid="chat-window"
      aria-label="Chat messages"
    >
      <div className="empty-state">No messages yet</div>
    </section>
  );
}

