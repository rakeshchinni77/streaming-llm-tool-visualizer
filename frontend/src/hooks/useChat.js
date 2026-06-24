import useChatStore from "../store/chatStore";
import streamClient from "../services/streamClient";

export default function useChat() {
	const addMessage = useChatStore((s) => s.addMessage);
	const appendAssistantDelta = useChatStore((s) => s.appendAssistantDelta);
	const setStreamingStatus = useChatStore((s) => s.setStreamingStatus);

	async function sendMessage(userText) {
		if (!userText || !userText.trim()) return;

		// Add user message immediately
		const userMessage = { id: String(Date.now()) + "-u", role: "user", content: userText };
		addMessage(userMessage);

		// Add empty assistant message to be filled
		const assistantMessage = { id: String(Date.now()) + "-a", role: "assistant", content: "" };
		addMessage(assistantMessage);

		setStreamingStatus("streaming");

		const messages = [
			{ role: "user", content: userText },
		];

		const abort = await streamClient.streamChat(
			messages,
			(delta) => {
				appendAssistantDelta(delta);
			},
			() => {
				setStreamingStatus("idle");
			},
			(err) => {
				console.error("Streaming error:", err);
				setStreamingStatus("idle");
				appendAssistantDelta("\nUnable to connect to server.");
			}
		);

		return abort;
	}

	return { sendMessage };
}
