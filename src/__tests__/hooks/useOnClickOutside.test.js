import { vi } from 'vitest';
import { renderHook } from '@testing-library/react-hooks';
import useOnClickOutside from '../../hooks/useOnClickOutside';

/**
 * @param{component? DOM node?} ref = useRef
 * @param{Function} handler - function to be called onClick if conditions are met
 *
 * Actual usage - closes a modal when you click outside the modal
 *
 * if the event emitted by the 'mousedown' listener added in the custom hook has a target
 * not contained in the DOM node tree of the ref passed in by useRef, handler function is called
 *
 * The hook and related modal components make heavy use of React Context, which I don't understand.
 * That might make testing harder, it might not. That being said, I should probably sort out what
 * exactly is happening here.
 *
 * Testing strategies:
 *
 * click happens outside ref context
 * it('handler() is called when domNode.not.includes(target of a mousedown event)')
 * click happens inside ref context
 * it('handler() is NOT called when domNode.includes(target of a mousedown event)')
 *
 */

// how to simulate a click outside the window
describe('useOnClickOutside', () => {
  const mockRefRoot = document.createElement('div').setAttribute('id', 'mock-ref-root');
  const mockModal = document.createElement('div').setAttribute('id', 'mock-modal');
  const click = new MouseEvent('mousedown');
  const mockEventTarget = document.createElement('div').setAttribute('id', 'mock-outside-modal');
  const mockHandler = vi.fn();

  renderHook(() => useOnClickOutside(mockRefRoot, mockHandler));
});
