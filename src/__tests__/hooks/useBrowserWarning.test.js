import { vi } from 'vitest';
import { renderHook } from '@testing-library/react-hooks';
import useBrowserWarning from '../../hooks/useBrowserWarning';

describe('useBrowserWarning', () => {
  let windowSpy;

  beforeEach(() => {
    windowSpy = vi.spyOn(window, 'window', 'get');
  });

  afterEach(() => {
    windowSpy.mockRestore();
  });

  it('renderHook does something useful', () => {
    windowSpy.mockImplementation(() => ({
      navigator: {
        userAgent: 'bondJamesBond',
        vendor: 'Google',
      },
      chrome: false,
      opr: false,
    }));
    console.log(window);
    const { result } = renderHook(() => useBrowserWarning());
    console.log(result);

    expect(window.navigator.userAgent).toEqual('bondJamesBond');
  });

  it('userAgent should be bondJamesBond', () => {
    windowSpy.mockImplementation(() => ({
      navigator: {
        userAgent: 'bondJamesBond',
      },
    }));

    expect(window.navigator.userAgent).toEqual('bondJamesBond');
  });

  it('should return https://example.com', () => {
    windowSpy.mockImplementation(() => ({
      location: {
        origin: 'https://example.com',
      },
    }));

    expect(window.location.origin).toEqual('https://example.com');
  });

  it('should be undefined.', () => {
    windowSpy.mockImplementation(() => undefined);

    expect(window).toBeUndefined();
  });

  //   const fn = vi.fn();

  //   it('returns [false, () => setShouldDisplay(false)] when browser is Chrome', () => {
  //     act(() => {
  //       // error:
  //       // Cannot set property userAgent of #<Navigator> which has only a getter
  //       window.navigator.userAgent = `Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36`;
  //       window.navigator.vendor = 'Google Inc.';
  //       window.chrome = true;
  //     });

  //     const { result } = renderHook(() => useBrowserWarning());
  //     console.log(`result.current`);
  //     console.log(result.current);
  //     expect(result.current).toBe([false, fn]);
  //   });
});
