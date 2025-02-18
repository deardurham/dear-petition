import { useState } from 'react';
import styled from 'styled-components';
import { offset as floatingOffset, useFloating, useFocus, useHover, useInteractions } from '@floating-ui/react';
import { Popover } from '@headlessui/react';

const TooltipContentWrapper = styled.div`
  display: flex;
  flex-direction: ${(props) => props.flexDirection};
  align-items: center;
  background: rgb(255 255 255);
  z-index: 10;
  filter: drop-shadow(0 10px 8px rgb(0 0 0 / 0.04)) drop-shadow(0 4px 3px rgb(0 0 0 / 0.1));
  border: 1px solid rgb(75 85 99);
  border-radius: 0.5rem;
  padding: 1rem 0.5rem;
`;

export const Tooltip = ({
  children,
  tooltipContent,
  placement,
  hideTooltip = false,
  offset = 0,
  flexDirection = 'row',
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const { refs, floatingStyles, context } = useFloating({
    open: isOpen,
    onOpenChange: setIsOpen,
    placement,
    middleware: [floatingOffset(offset)],
  });
  const hover = useHover(context);
  const focus = useFocus(context);
  const { getReferenceProps, getFloatingProps } = useInteractions([hover, focus]);
  if (hideTooltip) {
    return children;
  }
  return (
    <Popover>
      <div ref={refs.setReference} {...getReferenceProps()}>
        {children}
      </div>
      {isOpen && (
        <Popover.Panel static ref={refs.setFloating} style={floatingStyles} {...getFloatingProps()}>
          <TooltipContentWrapper flexDirection={flexDirection}>{tooltipContent}</TooltipContentWrapper>
        </Popover.Panel>
      )}
    </Popover>
  );
};
