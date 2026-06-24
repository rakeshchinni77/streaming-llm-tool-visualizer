import { create } from "zustand";

const useChatStore = create((set) => ({
  messages: [],
  activeToolCalls: [],
  tokenCount: 0,
  streamingStatus: "idle", // 'idle' | 'streaming'

  // Basic setters
  setMessages: (messages) => set({ messages }),
  setActiveToolCalls: (activeToolCalls) => set({ activeToolCalls }),
  setTokenCount: (tokenCount) => set({ tokenCount }),
  setStreamingStatus: (streamingStatus) => set({ streamingStatus }),

  // Helpers
  addMessage: (message) =>
    set((state) => ({ messages: [...state.messages, message] })),

  // Append assistant delta to the last assistant message
  appendAssistantDelta: (delta) =>
    set((state) => {
      const messages = [...state.messages];
      // Find last assistant message
      for (let i = messages.length - 1; i >= 0; i--) {
        if (messages[i].role === "assistant") {
          messages[i] = { ...messages[i], content: (messages[i].content || "") + delta };
          return { messages };
        }
      }
      // If no assistant message exists, create one
      const newAssistant = { id: String(Date.now()), role: "assistant", content: delta };
      messages.push(newAssistant);
      return { messages };
    }),
}));

export default useChatStore;
