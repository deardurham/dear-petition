import { render, waitFor } from '@testing-library/react';
import App from '../components/App';
import { test } from 'vitest';
import store from '../store';
import { Provider } from 'react-redux';

test('When the app starts it renders a log in button', async () => {
  const container = document.createElement('div');
  container.setAttribute('id', 'test-root');
  document.body.appendChild(container);
  const { getByText } = render(
    <Provider store={store}>
      <App />
    </Provider>,
    container,
  );
  await waitFor(() => expect(getByText('Log In')).toBeInTheDocument());
});
