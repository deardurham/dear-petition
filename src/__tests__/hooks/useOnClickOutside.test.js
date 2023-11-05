import { vi } from 'vitest';
import { renderHook } from '@testing-library/react-hooks';
import useOnClickOutside from '../../hooks/useOnClickOutside';

describe('useOnClickOutside', () => {
  it('should call the handler when clicking outside the ref', () => {
    const ref = { current: document.createElement('div') };
    const handler = vi.fn();

    renderHook(() => useOnClickOutside(ref, handler));

    const outsideElement = document.createElement('div');
    document.body.appendChild(outsideElement);

    const event = new MouseEvent('mousedown', {
      bubbles: true,
      cancelable: true,
    });
    outsideElement.dispatchEvent(event);

    expect(handler).toHaveBeenCalled();
  });

  it('should not call the handler when clicking inside the ref', () => {
    const ref = { current: document.createElement('div') };
    const handler = vi.fn();

    renderHook(() => useOnClickOutside(ref, handler));

    const insideElement = document.createElement('div');
    ref.current.appendChild(insideElement);

    const event = new MouseEvent('mousedown', {
      bubbles: true,
      cancelable: true,
    });
    insideElement.dispatchEvent(event);

    expect(handler).not.toHaveBeenCalled();
  });

  it('should not call the handler after hook is unmounted', () => {
    const ref = { current: document.createElement('div') };
    const handler = vi.fn();

    const { unmount } = renderHook(() => useOnClickOutside(ref, handler));

    const outsideElement = document.createElement('div');
    document.body.appendChild(outsideElement);

    const event = new MouseEvent('mousedown', {
      bubbles: true,
      cancelable: true,
    });

    outsideElement.dispatchEvent(event);
    expect(handler).toHaveBeenCalledTimes(1);

    unmount();

    outsideElement.dispatchEvent(event);
    expect(handler).toHaveBeenCalledTimes(1);
  });
});
