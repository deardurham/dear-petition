import React from 'react';
import { useModalContext } from '../Button/ModalButton';
import { Button } from '../Button';

export const DisplaySettingsModal = ({ children }) => {
  const { closeModal } = useModalContext();
  return (
    <div className="px-24 py-16 flex flex-col gap-8">
      <h2 className="self-center">Settings</h2>
      {children}
      <Button className="self-center w-fit px-6 py-2" onClick={() => closeModal()}>
        Close
      </Button>
    </div>
  );
};
