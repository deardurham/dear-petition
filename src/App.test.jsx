import { render, screen } from '@testing-library/react';
import App from './components/App';

it('renders login page', () => {
  render(<App />);
  expect(screen.getByText('username')).toBeInTheDocument();
});
