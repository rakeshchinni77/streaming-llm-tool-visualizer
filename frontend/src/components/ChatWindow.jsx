import React from "react";
import useChatStore from "../store/chatStore";

export default function ChatWindow() {
  const messages = useChatStore((state) => state.messages);

  return (
    <section
      className="card chat-window"
      data-testid="chat-window"
      aria-label="Chat messages"
    >
      {messages.length === 0 ? (
        <div className="empty-state">No messages yet</div>
      ) : (
        <div className="message-list">
          {messages.map((message) => (
            <div key={message.id} className="message-row">
              <div className="message-role">
                {message.role === "user" ? "User" : "Assistant"}:
              </div>
              <div className="message-content">{message.content}</div>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}

