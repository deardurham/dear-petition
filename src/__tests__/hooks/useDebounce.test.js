import { vi } from 'vitest';
import { renderHook } from '@testing-library/react-hooks';
import useDebounce from '../../hooks/useDebounce';

describe('useDebounce', () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('should debounce the callback function', async () => {
    const callback = vi.fn(() => console.log('callback called'));
    const { result, rerender } = renderHook(() => useDebounce(callback, { timeout: 500 }));

    // Call the debounced function multiple times within a short period
    result.current('call 1');
    result.current('call 2');
    result.current('call 3');

    rerender({ timeout: 1000 });
    vi.runAllTimers();
    // Ensure that the callback has been called only once with the last argument
    expect(callback).toHaveBeenCalledTimes(1);
    expect(callback).toHaveBeenCalledWith('call 3');
  });
});
