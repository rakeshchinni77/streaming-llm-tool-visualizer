import React from "react";
import useChatStore from "../store/chatStore";
import Message from "./Message";

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
            <Message key={message.id} message={message} />
          ))}
        </div>
      )}
    </section>
  );
}

