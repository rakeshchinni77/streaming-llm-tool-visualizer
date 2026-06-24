import React from "react";

export default function Message({ message }) {
  if (!message) return null;

  const isAssistant = message.role === "assistant";
  const roleLabel = isAssistant ? "Assistant" : "User";

  return (
    <div className="message-row" data-testid={`message-${message.id}`}>
      <div className="message-role">{roleLabel}:</div>
      {isAssistant ? (
        <div className="message-content" data-testid="assistant-message-text">
          {message.content}
        </div>
      ) : (
        <div className="message-content">{message.content}</div>
      )}
    </div>
  );
}
