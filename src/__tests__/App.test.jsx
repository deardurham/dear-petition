import { act, render, screen } from '@testing-library/react';
import App from '../components/App';
import { test } from 'vitest';

test('When the app starts it renders a log in button', () => {
  const container = document.createElement('div');
  container.setAttribute('id', 'test-root');
  document.body.appendChild(container);

  act(() => {
    render(<App />, container);
  });

  const loginElement = screen.getByText('Log In');
  expect(loginElement).toBeInTheDocument();
});
