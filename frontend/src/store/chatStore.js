import { create } from "zustand";

const useChatStore = create((set) => ({
  messages: [],
  activeToolCalls: [],
  completedToolCalls: [],
  tokenCount: 0,
  streamingStatus: "idle", // 'idle' | 'streaming'

  // Basic setters
  setMessages: (messages) => set({ messages }),
  setActiveToolCalls: (activeToolCalls) => set({ activeToolCalls }),
  setCompletedToolCalls: (completedToolCalls) => set({ completedToolCalls }),
  setTokenCount: (tokenCount) => set({ tokenCount }),
  setStreamingStatus: (streamingStatus) => set({ streamingStatus }),

  // Helpers
  addMessage: (message) =>
    set((state) => ({ messages: [...state.messages, message] })),
  addToolCall: (toolCall) =>
    set((state) => {
      if (state.activeToolCalls.some((call) => call.id === toolCall.id)) {
        return state;
      }

      const messages = [...state.messages];
      const insertIndex = messages.findIndex((msg) => msg.role === "assistant");
      if (insertIndex === -1) {
        messages.push(toolCall);
      } else {
        messages.splice(insertIndex, 0, toolCall);
      }

      return {
        activeToolCalls: [...state.activeToolCalls, toolCall],
        messages,
      };
    }),
  updateToolCall: (toolId, updates) =>
    set((state) => {
      let completedToolCalls = [...state.completedToolCalls];
      const activeToolCalls = state.activeToolCalls
        .map((call) => {
          if (call.id !== toolId) return call;
          const updatedCall = { ...call, ...updates };
          if (updatedCall.status && updatedCall.status !== "Running") {
            completedToolCalls = [...completedToolCalls, updatedCall];
            return null;
          }
          return updatedCall;
        })
        .filter(Boolean);

      const messages = state.messages.map((message) => {
        if (message.type === "tool_call" && message.id === `tool-${toolId}`) {
          return { ...message, ...updates };
        }
        return message;
      });

      return {
        activeToolCalls,
        completedToolCalls,
        messages,
      };
    }),

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
