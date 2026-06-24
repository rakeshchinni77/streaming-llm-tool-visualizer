import React from "react";
import ContextMonitor from "../components/ContextMonitor";
import ChatWindow from "../components/ChatWindow";
import ChatInput from "../components/ChatInput";

export default function ChatPage() {
  return (
    <main className="app-shell">
      <header className="app-header">
        <div>
          <p className="eyebrow">Streaming LLM Tool Visualizer</p>
          <h1>LLM Chat Interface</h1>
        </div>
      </header>

      <ContextMonitor />

      <section className="chat-layout">
        <ChatWindow />
        <ChatInput />
      </section>
    </main>
  );
}

