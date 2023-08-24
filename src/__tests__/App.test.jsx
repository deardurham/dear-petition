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

// Testing vitest to make sure it will run a very basic test correctly (spoiler, it does)
// npm run test
// test('1 + 1 = 2', () => {
//   const sum = (x, y) => x + y;
//   expect(sum(1, 1)).toEqual(2);
// });
