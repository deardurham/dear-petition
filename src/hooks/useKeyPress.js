import { useEffect } from 'react';
/**
 * useKeyPress
 * @param {string} key - the name of the key to respond to, compared against event.key
 * @param {function} action - the action to perform on key press
 */
const useKeyPress = (key, action) => {
    useEffect(() => {
        function handleKeyPress(e) {
            if (e.key === key) action();
        }
        window.addEventListener('keyup', handleKeyPress);
        console.log("Added event listener");
        return () => window.removeEventListener('keyup', handleKeyPress);
    }, [key]);
};

export default useKeyPress;
