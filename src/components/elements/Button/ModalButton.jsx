import React, { useCallback, useRef, useState } from 'react';
import { Button } from './Button';
import StyledDialog from '../Modal/Dialog';
import useOnClickOutside from '../../../hooks/useOnClickOutside';

const ModalContext = React.createContext();

export const useModalContext = () => {
  const context = React.useContext(ModalContext);
  if (context === undefined) {
    throw new Error('useModal must be used within a ModalProvider');
  }
  return context;
};

export const ModalButton = ({ children, className, colorClass, title, allowCloseOnEscape = false }) => {
  const modalElement = useRef();
  const buttonElement = useRef();

  const [showModal, setShowModal] = useState(false);
  const closeModal = useCallback(() => setShowModal(false), []);
  useOnClickOutside(modalElement, () => {
    if (!allowCloseOnEscape) {
      closeModal();
    }
  });
  const handleClick = (e) => {
    // ignore click if it's been propogated from child
    if (!buttonElement.current?.contains(e.target)) {
      return;
    }
    setShowModal(true);
  };
  return (
    <Button ref={buttonElement} className={className} colorClass={colorClass ?? 'neutral'} onClick={handleClick}>
      {title}
      <ModalContext.Provider value={{ closeModal }}>
        <StyledDialog isOpen={showModal} onClose={allowCloseOnEscape ? closeModal : undefined}>
          <div ref={modalElement}>{children}</div>
        </StyledDialog>
      </ModalContext.Provider>
    </Button>
  );
};
