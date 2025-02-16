import { renderHook } from '@testing-library/react';
import usePortal from '../../hooks/usePortal';

describe('usePortal', () => {
  it('inserts an empty div into DOM with correct ID', () => {
    const sibling = document.createElement('section');
    document.body.insertAdjacentElement('beforeend', sibling);

    const { result } = renderHook(() => usePortal('usePortal-test'));
    const portal = result.current;
    const portalId = document.querySelector('#usePortal-test').id;

    expect(portal).toBeInTheDocument();
    expect(portal).toBeEmptyDOMElement();
    expect(portalId).toBe(`usePortal-test`);
  });
});
