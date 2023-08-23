import useWindowSize from '../../hooks/useWindowSize';
import { renderHook } from '@testing-library/react-hooks';

describe('window resize hook', () => {
  it('sets state to initial window size', () => {
    const { result } = renderHook(() => useWindowSize());

    expect(result.current.height).not.toBeUndefined();
    expect(result.current.width).not.toBeUndefined();
    expect(result.current.height).toBeGreaterThan(1);
    expect(result.current.width).toBeGreaterThan(1);
  });
});
