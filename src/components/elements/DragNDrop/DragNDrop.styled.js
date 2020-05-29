import styled from 'styled-components';
import { colorGrey, colorPrimary } from '../../../styles/colors';
import { motion } from 'framer-motion';

export const FileInputStyled = styled.input`
  width: 0.1px;
  height: 0.1px;
  opacity: 0;
  overflow: hidden;
  position: absolute;
  z-index: -1;
`;

export const DragNDropStyled = styled(motion.label)`
  cursor: pointer;
  border-radius: 2px;
  border: 5px dashed ${(props) => (props.draggedOver ? colorPrimary : colorGrey)};
  min-height: 5px;
  min-width: 5px;
`;
