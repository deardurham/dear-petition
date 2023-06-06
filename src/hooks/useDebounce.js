import { useCallback, useEffect, useRef } from 'react';

const useDebounce = (callback, { timeout }) => {
  const timer = useRef();

  useEffect(() => timer.current && clearTimeout(timer.current), []);

  return useCallback(
    (args) => {
      if (timer.current) {
        clearTimeout(timer.current);
      }
      timer.current = setTimeout(() => callback(args), timeout ?? 500);
    },
    [callback, timeout],
  );
};

export default useDebounce;
