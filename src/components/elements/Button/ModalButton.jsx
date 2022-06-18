import React, { useCallback, useState } from 'react';
import { Button } from './Button';
import StyledDialog from '../Modal/Dialog';

const ModalContext = React.createContext();

export const useModalContext = () => {
  const context = React.useContext(ModalContext);
  if (context === undefined) {
    throw new Error('useModal must be used within a ModalProvider');
  }
  return context;
};

export const ModalButton = ({ children, className, colorClass, title }) => {
  const [showModal, setShowModal] = useState(false);
  const closeModal = useCallback(() => setShowModal(false));
  return (
    <Button
      className={className}
      colorClass={colorClass ?? 'neutral'}
      onClick={() => setShowModal(true)}
    >
      {title}
      <ModalContext.Provider value={{ closeModal }}>
        <StyledDialog isOpen={showModal} onClose={closeModal}>
          {children}
        </StyledDialog>
      </ModalContext.Provider>
    </Button>
  );
};
