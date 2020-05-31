import React from 'react';
import ReactDOM from 'react-dom';
import { ModalStyled, ModalUnderlay } from './Modal.styled';

// Hooks
import usePortal from '../../../hooks/usePortal';

function Modal({ children, isVisible, closeModal, ...props }) {
  const modalPortal = usePortal('modal-root');
  return ReactDOM.createPortal(
    <>
      {isVisible && [
        <ModalUnderlay key="shade" onClick={closeModal}></ModalUnderlay>,
        <ModalStyled key="modal" {...props}>
          {children}
        </ModalStyled>
      ]}
    </>,
    modalPortal
  );
}

export default Modal;
