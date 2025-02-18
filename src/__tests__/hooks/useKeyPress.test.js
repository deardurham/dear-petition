import { vi } from 'vitest';
import { renderHook } from '@testing-library/react';
import useKeyPress from '../../hooks/useKeyPress';

describe('useKeyPress', () => {
  it('should call the action function on Enter key press', () => {
    const key = 'Enter';
    const action = vi.fn();

    renderHook(() => useKeyPress(key, action));
    const event = new KeyboardEvent('keyup', { key });
    window.dispatchEvent(event);

    expect(action).toHaveBeenCalledTimes(1);
  });

  it('should not call the action function on Escape key press', () => {
    const key = 'Enter';
    const action = vi.fn();

    renderHook(() => useKeyPress(key, action));
    const event = new KeyboardEvent('keyup', { key: 'Escape' });
    window.dispatchEvent(event);

    expect(action).not.toHaveBeenCalled();
  });

  it('action is not triggered after hook is unmounted', () => {
    const key = 'Enter';
    const action = vi.fn();

    const { unmount } = renderHook(() => useKeyPress(key, action));
    unmount();
    const event = new KeyboardEvent('keyup', { key });
    window.dispatchEvent(event);

    expect(action).not.toHaveBeenCalled();
  });
});
