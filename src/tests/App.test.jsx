// import { render, screen } from '@testing-library/react';
// import App from './components/App';

// it('renders login page', () => {
//   render(<App />);
//   expect(screen.getByText('username')).toBeInTheDocument();
// });

import App from '../components/App';
import { it, describe } from 'vitest';
import { render, screen } from '@testing-library/react';

describe('App.js', () => {
  it('Check if the App renders even a tiny bit plz', () => {
    //render our App properly
    render(<App />);
    const username = screen.getByText('username');
    expect(username).toBeInTheDocument();

    // screen.debug();
  });
});
