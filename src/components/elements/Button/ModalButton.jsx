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

export const ModalButton = ({
  children,
  className,
  colorClass,
  title,
  allowCloseOnEscape = false,
}) => {
  const modalElement = useRef();
  const [showModal, setShowModal] = useState(false);
  const closeModal = useCallback(() => setShowModal(false));
  useOnClickOutside(modalElement, () => {
    if (!allowCloseOnEscape) {
      closeModal();
    }
  });
  return (
    <Button
      className={className}
      colorClass={colorClass ?? 'neutral'}
      onClick={() => setShowModal(true)}
    >
      {title}
      <ModalContext.Provider value={{ closeModal }}>
        <StyledDialog isOpen={showModal} onClose={allowCloseOnEscape ? closeModal : undefined}>
          <div ref={modalElement}>{children}</div>
        </StyledDialog>
      </ModalContext.Provider>
    </Button>
  );
};
