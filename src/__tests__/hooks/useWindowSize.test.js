import useWindowSize from '../../hooks/useWindowSize';
import { vi } from 'vitest';
import { renderHook } from '@testing-library/react-hooks';

describe('useWindowSize', () => {
  it('sets state to an initial window size', () => {
    vi.stubGlobal('innerWidth', 1920);
    vi.stubGlobal('innerHeight', 1080);

    const { result } = renderHook(() => useWindowSize());

    expect(result.current.width).toBe(1920);
    expect(result.current.height).toBe(1080);

    vi.unstubAllGlobals();
  });

  it('adjusts after window resize event', () => {
    vi.stubGlobal('innerWidth', 1920);
    vi.stubGlobal('innerHeight', 1080);

    const { result } = renderHook(() => useWindowSize());

    expect(result.current.width).toBe(1920);
    expect(result.current.height).toBe(1080);

    window.innerWidth = 1280;
    window.innerHeight = 720;
    window.dispatchEvent(new Event('resize'));

    expect(result.current.width).toBe(1280);
    expect(result.current.height).toBe(720);

    vi.unstubAllGlobals();
  });
});
