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
    const callback = vi.fn((_arg) => console.log());
    const { result } = renderHook(() => useDebounce(callback, { timeout: 500 }));

    // Call the debounced function multiple times within a short period
    result.current('call 1');
    result.current('call 2');
    result.current('call 3');

    vi.runAllTimers();

    // Ensure that the callback has been called only once with the last argument
    expect(callback).toHaveBeenCalledTimes(1);
    expect(callback).toHaveBeenCalledWith('call 3');
  });

  it('should not execute the function until timer exceeds timeout', () => {
    const callback = vi.fn((_arg) => console.log());
    const { result } = renderHook(() => useDebounce(callback, { timeout: 500 }));

    result.current('call 1');

    // advancing by 2ms won't trigger callback
    vi.advanceTimersByTime(2);
    expect(callback).not.toHaveBeenCalled();
    // advancing by 500ms total will trigger callback
    vi.advanceTimersByTime(498);
    expect(callback).toHaveBeenCalled();
  });
});
