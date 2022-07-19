import { useEffect, useRef } from 'react';

export default function useOnClickOutside(ref, handler) {
  const stableHandlerCallback = useRef(handler);
  useEffect(() => {
    const onClick = (event) => {
      if (ref.current && !ref.current.contains(event.target)) {
        stableHandlerCallback.current();
      }
    };
    document.addEventListener('mousedown', onClick);

    return () => {
      document.removeEventListener('mousedown', onClick);
    };
  }, [ref]);
}
