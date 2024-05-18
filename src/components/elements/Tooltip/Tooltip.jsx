import { useRef, useState } from 'react';
import { Popover } from '@headlessui/react';
import { usePopper } from 'react-popper';
import styled from 'styled-components';

const TooltipContentWrapper = styled.div`
  display: flex;
  align-items: center;
  background: rgb(255 255 255);
  z-index: 10;
  filter: drop-shadow(0 10px 8px rgb(0 0 0 / 0.04)) drop-shadow(0 4px 3px rgb(0 0 0 / 0.1));
  border: 1px solid rgb(75 85 99);
  border-radius: 0.5rem;
  padding: 1rem 0.5rem;
`;

export const Tooltip = ({ children, tooltipContent, placement, hideTooltip = false, offset = [0, 0] }) => {
  const hoverDiv = useRef(null);
  const [isHovering, setIsHovering] = useState(false);
  const [popperElement, setPopperElement] = useState();
  const { styles, attributes } = usePopper(hoverDiv.current, popperElement, {
    placement,
    modifiers: {
      name: 'offset',
      options: {
        offset,
      },
    },
  });
  if (hideTooltip) {
    return children;
  }
  return (
    <Popover>
      <div
        ref={hoverDiv}
        onMouseEnter={() => {
          setIsHovering(true);
        }}
        onMouseLeave={() => setIsHovering(false)}
      >
        {children}
      </div>
      {isHovering && (
        <Popover.Panel static ref={setPopperElement} style={styles.popper} {...attributes.popper}>
          <TooltipContentWrapper>{tooltipContent}</TooltipContentWrapper>
        </Popover.Panel>
      )}
    </Popover>
  );
};
