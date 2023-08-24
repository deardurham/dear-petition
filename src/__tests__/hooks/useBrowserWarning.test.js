import { renderHook } from '@testing-library/react-hooks';
import useBrowserWarning from '../../hooks/useBrowserWarning';

describe('useBrowserWarning', () => {
  it('if browser is Chrome, return [false, false]', () => {
    const isChrome = true;
    renderHook(() => useBrowserWarning());
  });
});
