import React, { useEffect } from 'react';
import ReactDOM from 'react-dom';
import { ModalStyled, ModalUnderlay } from './Modal.styled';

// Hooks
import usePortal from '../../../hooks/usePortal';

function Modal({ children, isVisible, closeModal, ...props }) {
  const modalPortal = usePortal('modal-root');

  // Disable scrolling while modal is open
  useEffect(() => {
    document.body.style.overflow = isVisible ? 'hidden' : 'unset';
    return () => {
      document.body.style.overflow = 'unset';
    };
  }, [isVisible]);

  return ReactDOM.createPortal(
    <>
      {isVisible && [
        <ModalUnderlay key="shade" onClick={closeModal} />,
        <ModalStyled key="modal" {...props}>
          {children}
        </ModalStyled>,
      ]}
    </>,
    modalPortal
  );
}

export default Modal;
