// import { render, screen } from '@testing-library/react';
// import App from './components/App';

// it('renders login page', () => {
//   render(<App />);
//   expect(screen.getByText('username')).toBeInTheDocument();
// });

// import App from '../components/App';
// import HelpPage from '../components/pages/HelpPage/HelpPage';
// import { it, describe, test } from 'vitest';
import { test } from 'vitest';
// import { render, screen } from '@testing-library/react';

test('1 + 1 = 2', () => {
  const sum = (x, y) => x + y;
  expect(sum(1, 1)).toEqual(2);
});

// describe('App.js', () => {
//   it('Check if the App renders even a tiny bit plz', () => {
//     //render our App properly
//     render(<HelpPage />);
//     const contact = screen.getByText('Contact');
//     expect(contact).toBeInTheDocument();
//     screen.debug();
//   });
// });
