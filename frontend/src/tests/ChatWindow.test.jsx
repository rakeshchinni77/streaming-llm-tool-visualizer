import { render, screen } from '@testing-library/react';
import ChatWindow from '../components/ChatWindow';
import useChatStore from '../store/chatStore';

describe('ChatWindow', () => {
  beforeEach(() => {
    useChatStore.setState({ messages: [] });
  });

  it('renders messages from the store', () => {
    useChatStore.setState({
      messages: [{ id: '1', role: 'assistant', content: 'Hello there' }],
    });

    render(<ChatWindow />);

    expect(screen.getByText('Hello there')).toBeInTheDocument();
  });
});
