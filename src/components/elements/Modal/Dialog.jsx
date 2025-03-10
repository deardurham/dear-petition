import { DialogPanel, Dialog as HeadlessuiDialog } from '@headlessui/react';

// This component doesn't use our other modal code and instead uses headless ui
// My goal is to make a comopnent that's easier to style. We'll see if that works out
export const Dialog = ({ children, isOpen, onClose }) => (
  <HeadlessuiDialog open={isOpen} onClose={() => onClose()} className="fixed z-15 inset-0 overflow-y-auto">
    <div className="fixed inset-0 bg-black opacity-30" />
    <DialogPanel>
      <div className="flex items-center justify-center min-h-screen">
        <div className="relative bg-white rounded mx-auto">{children}</div>
      </div>
    </DialogPanel>
  </HeadlessuiDialog>
);

export default Dialog;
