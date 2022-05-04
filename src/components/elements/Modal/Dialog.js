import React from 'react';
import { Dialog } from '@headlessui/react';

// This component doesn't use our other modal code and instead uses headless ui
// My goal is to make a comopnent that's easier to style. We'll see if that works out
const CenteredDialog = ({ children, isOpen, onClose }) => (
  <Dialog open={isOpen} onClose={() => onClose()} className="fixed z-15 inset-0 overflow-y-auto">
    <div className="flex items-center justify-center min-h-screen">
      <Dialog.Overlay className="fixed inset-0 bg-black opacity-30" />
      <div className="relative bg-white rounded mx-auto">{children}</div>
    </div>
  </Dialog>
);

export default CenteredDialog;
