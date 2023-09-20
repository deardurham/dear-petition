import { renderHook } from '@testing-library/react-hooks';
import usePortal from '../../hooks/usePortal';

describe('usePortal', () => {
  it('makes a div', () => {
    const sibling = document.createElement('section');
    sibling.innerText = `I'm a sibling section`;
    document.body.insertAdjacentElement('beforeend', sibling);

    const { result } = renderHook(() => usePortal('usePortal-test'));
    const portal = document.querySelector('#usePortal-test');
    portal.innerText = `I'm a portal! The cake is a lie, etc.`;

    console.log('portal');
    console.log(portal.innerText);

    console.log('sibling');
    console.log(sibling.innerText);

    expect(result.current).toBeInTheDocument();
    expect(result.current).toBeEmptyDOMElement();
    expect(result.current).toHaveTextContent(`I'm a portal! The cake is a lie, etc.`);
  });
});
