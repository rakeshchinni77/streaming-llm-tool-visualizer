import React, { useState } from "react";
import useChatStore from "../store/chatStore";

export default function ChatInput() {
  const [text, setText] = useState("");
  const streamingStatus = useChatStore((state) => state.streamingStatus);
  const disabled = streamingStatus !== "idle";

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
        disabled={disabled}
      />

      <button type="button" disabled={disabled}>
        Send
      </button>
    </form>
  );
}

