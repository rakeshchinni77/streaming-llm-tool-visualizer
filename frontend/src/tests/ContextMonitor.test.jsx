import { fireEvent, render, screen } from '@testing-library/react';
import ContextMonitor from '../components/ContextMonitor';
import useChatStore from '../store/chatStore';

vi.mock('../services/api', () => ({
  summarizeConversation: vi.fn().mockResolvedValue({ summary: 'A summary' }),
}));

describe('ContextMonitor', () => {
  beforeEach(() => {
    useChatStore.setState({ tokenCount: 42, messages: [] });
  });

  it('renders token count and compress button', () => {
    render(<ContextMonitor />);

    expect(screen.getByTestId('context-monitor')).toBeInTheDocument();
    expect(screen.getByTestId('total-tokens')).toHaveTextContent('Tokens: 42');
    expect(screen.getByTestId('compress-button')).toBeInTheDocument();
  });

  it('invokes the compress action when clicked', async () => {
    render(<ContextMonitor />);

    fireEvent.click(screen.getByTestId('compress-button'));

    expect(await screen.findByTestId('compress-button')).toBeInTheDocument();
  });
});
