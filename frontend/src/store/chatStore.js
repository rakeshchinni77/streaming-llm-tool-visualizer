import { create } from "zustand";

const useChatStore = create((set) => ({
  messages: [
    {
      id: "1",
      role: "user",
      content: "Hello AI",
    },
    {
      id: "2",
      role: "assistant",
      content: "Hello! How can I help you?",
    },
  ],
  activeToolCalls: [],
  tokenCount: 42,
  streamingStatus: "idle",

  setMessages: (messages) => set({ messages }),
  setActiveToolCalls: (activeToolCalls) => set({ activeToolCalls }),
  setTokenCount: (tokenCount) => set({ tokenCount }),
  setStreamingStatus: (streamingStatus) => set({ streamingStatus }),
}));

export default useChatStore;
