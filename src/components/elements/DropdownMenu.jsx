import React, { useState } from 'react';
import { useFloating, useFocus, useInteractions } from '@floating-ui/react';
import { Menu } from '@headlessui/react';

export const DropdownMenu = ({ children, items }) => {
  const [isHovering, setIsHovering] = useState(false);
  const { refs, floatingStyles, context } = useFloating({
    open: isHovering,
    onOpenChange: setIsHovering,
    placement: 'bottom',
  });
  const focus = useFocus(context);
  const { getReferenceProps, getFloatingProps } = useInteractions([focus]);
  return (
    <Menu as="div" className="relative" onMouseLeave={() => setIsHovering(false)}>
      <Menu.Button>
        <div
          ref={refs.setReference}
          {...getReferenceProps()}
          onMouseEnter={() => {
            setIsHovering(true);
          }}
        >
          {children}
        </div>
      </Menu.Button>
      <Menu.Items
        as="div"
        static
        ref={refs.setFloating}
        style={floatingStyles}
        {...getFloatingProps()}
        className="absolute z-10 bg-white min-w-full"
      >
        {isHovering && (
          <div>
            {React.Children.map(items, (item) => (
              <Menu.Item as="div">{() => item}</Menu.Item>
            ))}
          </div>
        )}
      </Menu.Items>
    </Menu>
  );
};
