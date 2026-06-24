import React, { useState } from "react";
import useChatStore from "../store/chatStore";
import useChat from "../hooks/useChat";

export default function ChatInput() {
  const [text, setText] = useState("");
  const streamingStatus = useChatStore((state) => state.streamingStatus);
  const disabled = streamingStatus !== "idle";
  const { sendMessage } = useChat();

  const submit = async (e) => {
    e && e.preventDefault();
    const value = text?.trim();
    if (!value) return;
    setText("");
    try {
      await sendMessage(value);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <form data-testid="chat-input" className="card chat-input-form" onSubmit={submit}>
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
        onKeyDown={(e) => {
          if (e.key === "Enter" && !e.shiftKey) {
            submit(e);
          }
        }}
      />

      <button type="submit" disabled={disabled}>
        Send
      </button>
    </form>
  );
}

