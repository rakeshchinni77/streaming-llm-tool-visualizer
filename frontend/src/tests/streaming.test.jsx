import { fireEvent, render, screen } from '@testing-library/react';
import useChatStore from '../store/chatStore';
import useChat from '../hooks/useChat';

const { streamChatMock } = vi.hoisted(() => ({
  streamChatMock: vi.fn(),
}));

vi.mock('../services/streamClient', () => ({
  default: { streamChat: streamChatMock },
}));

describe('streaming hook', () => {
  beforeEach(() => {
    useChatStore.setState({ messages: [], streamingStatus: 'idle' });
    streamChatMock.mockReset();
  });

  it('updates assistant content when streaming', async () => {
    streamChatMock.mockImplementation(async (_messages, onDelta, onDone) => {
      onDelta('Hello');
      onDone({ totalTokens: 1 });
      return () => {};
    });

    function Harness() {
      const { sendMessage } = useChat();
      const messages = useChatStore((state) => state.messages);

      return (
        <div>
          <button onClick={() => sendMessage('Hi')}>Send</button>
          <div>{messages.map((message) => <div key={message.id}>{message.content}</div>)}</div>
        </div>
      );
    }

    render(<Harness />);
    fireEvent.click(screen.getByRole('button', { name: /send/i }));

    expect(await screen.findByText(/Hello/i)).toBeInTheDocument();
  });
});
