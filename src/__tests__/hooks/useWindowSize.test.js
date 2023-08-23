import useWindowSize from '../../hooks/useWindowSize';
import { renderHook } from '@testing-library/react-hooks';

describe('window resize hook', () => {
  it('hook sets state to initial window size when called', () => {
    const { result } = renderHook(() => useWindowSize());

    expect(result.current.height).not.toBeUndefined();
    expect(result.current.width).not.toBeUndefined();
  });
});
