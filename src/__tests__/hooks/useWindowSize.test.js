import useWindowSize from '../../hooks/useWindowSize';
import { vi } from 'vitest';
import { act, renderHook } from '@testing-library/react';

describe('useWindowSize', () => {
  beforeEach(() => {
    vi.stubGlobal('innerWidth', 1920);
    vi.stubGlobal('innerHeight', 1080);
  });

  it('sets state to an initial window size', () => {
    const { result } = renderHook(() => useWindowSize());

    expect(result.current.width).toBe(1920);
    expect(result.current.height).toBe(1080);

    vi.unstubAllGlobals();
  });

  it('adjusts after window resize event', () => {
    const { result } = renderHook(() => useWindowSize());

    expect(result.current.width).toBe(1920);
    expect(result.current.height).toBe(1080);

    act(() => {
      window.innerWidth = 1280;
      window.innerHeight = 720;
      window.dispatchEvent(new Event('resize'));
    });

    expect(result.current.width).toBe(1280);
    expect(result.current.height).toBe(720);

    vi.unstubAllGlobals();
  });
});
