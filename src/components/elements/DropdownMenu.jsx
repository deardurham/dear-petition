import React, { useRef, useState } from 'react';
import { Menu } from '@headlessui/react';
import { usePopper } from 'react-popper';

export const DropdownMenu = ({ children, items }) => {
  const hoverDiv = useRef(null);
  const [isHovering, setIsHovering] = useState(false);
  const [popperElement, setPopperElement] = useState();
  const { styles, attributes } = usePopper(hoverDiv.current, popperElement, {
    placement: 'bottom',
  });
  return (
    <Menu as="div" className="relative" onMouseLeave={() => setIsHovering(false)}>
      <Menu.Button>
        <div
          ref={hoverDiv}
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
        ref={setPopperElement}
        style={styles.popper}
        {...attributes.popper}
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
