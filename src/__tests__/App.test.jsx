/*
// This was the code originally in the test file

import { render, screen } from '@testing-library/react';
import App from './components/App';
it('renders login page', () => {
    render(<App />);
    expect(screen.getByText('username')).toBeInTheDocument();
  });
*/

import { render, screen } from '@testing-library/react';
import App from '../components/App';

test('When the app starts it renders a log in button', () => {
  render(<App />);
  const loginElement = screen.getByText('Log In');
  expect(loginElement).toBeInTheDocument();
});

/*
// Testing vitest to make sure it will run a very basic test correctly (spoiler, it does)
// npm run test
import { test } from 'vitest';
test('1 + 1 = 2', () => {
  const sum = (x, y) => x + y;
  expect(sum(1, 1)).toEqual(2);
});

import { render, screen } from '@testing-library/react';
// import userEvent from '@testing-library/user-event';
import '@testing-library/jest-dom';
import App from '../components/App';

test('loads and displays login button', async () => {
  // ARRANGE
  render(<App />);

  // ACT
  // await userEvent.click(screen.getByText('Load Greeting'));
  const loginButton = screen.getByText('Log In');

  // ASSERT
  expect(loginButton).toHaveTextContent('Log In');
  expect(screen.getByRole('button')).toBeEnabled();
});

*/
