// import { setWindowProps } from '../util/isChrome.test';
import { vi } from 'vitest';
import { act, renderHook } from '@testing-library/react-hooks';
import useBrowserWarning from '../../hooks/useBrowserWarning';

describe('useBrowserWarning', () => {
  const fn = vi.fn();

  it('returns [false, () => setShouldDisplay(false)] when browser is Chrome', () => {
    act(() => {
      // error:
      // Cannot set property userAgent of #<Navigator> which has only a getter
      window.navigator.userAgent = `Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36`;
      window.navigator.vendor = 'Google Inc.';
      window.chrome = true;
    });

    const { result } = renderHook(() => useBrowserWarning());
    console.log(`result.current`);
    console.log(result.current);
    expect(result.current).toBe([false, fn]);
  });
});
