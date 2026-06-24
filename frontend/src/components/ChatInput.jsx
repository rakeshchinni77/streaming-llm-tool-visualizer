import React, { useState } from "react";

export default function ChatInput() {
  const [text, setText] = useState("");

  return (
    <form
      data-testid="chat-input"
      className="card chat-input-form"
      onSubmit={(e) => e.preventDefault()}
    >
      <label htmlFor="chat-text" className="visually-hidden">
        Type a message
      </label>

      <input
        id="chat-text"
        aria-label="Type a message"
        value={text}
        placeholder="Type a message..."
        onChange={(e) => setText(e.target.value)}
        type="text"
      />

      <button type="button" disabled>
        Send
      </button>
    </form>
  );
}

