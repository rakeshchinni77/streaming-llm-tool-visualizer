import { render, screen } from '@testing-library/react';
import ToolCallBlock from '../components/ToolCallBlock';

describe('ToolCallBlock', () => {
  it('renders tool information and status', () => {
    const message = {
      tool: 'calculator',
      status: 'Completed',
      input: { expression: '50 * 12' },
      result: { value: '600' },
      error: null,
    };

    render(<ToolCallBlock message={message} />);

    expect(screen.getByTestId('tool-call-block')).toBeInTheDocument();
    expect(screen.getByTestId('tool-name')).toHaveTextContent('calculator');
    expect(screen.getByTestId('tool-input')).toBeInTheDocument();
    expect(screen.getByTestId('tool-result')).toBeInTheDocument();
    expect(screen.getByText('Completed')).toBeInTheDocument();
  });
});
