import { useCallback, useEffect, useRef } from 'react';

const useDebounce = (callback, { timeout }) => {
  const timer = useRef();

  useEffect(() => timer.current && clearTimeout(timer.current), [timer]);

  return useCallback(
    (args) => {
      if (timer.current) {
        clearTimeout(timer.current);
      }
      timer.current = setTimeout(() => callback(args), timeout ?? 500);
    },
    [callback]
  );
};

export default useDebounce;
