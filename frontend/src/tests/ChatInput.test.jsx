import { fireEvent, render, screen } from '@testing-library/react';
import ChatInput from '../components/ChatInput';
import useChatStore from '../store/chatStore';

const sendMessage = vi.fn();

vi.mock('../hooks/useChat', () => ({
  default: () => ({ sendMessage }),
}));

describe('ChatInput', () => {
  beforeEach(() => {
    useChatStore.setState({ streamingStatus: 'idle' });
    sendMessage.mockReset();
  });

  it('updates the textbox and submits the message', async () => {
    sendMessage.mockResolvedValue(undefined);

    render(<ChatInput />);

    const input = screen.getByLabelText(/type a message/i);
    fireEvent.change(input, { target: { value: 'Hello' } });

    expect(input.value).toBe('Hello');

    fireEvent.submit(screen.getByTestId('chat-input'));

    expect(sendMessage).toHaveBeenCalledWith('Hello');
  });
});
