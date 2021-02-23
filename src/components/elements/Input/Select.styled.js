import styled from 'styled-components';
import Select from 'react-select';
import { motion } from 'framer-motion';
import { colorRed } from '../../../styles/colors';

export const SelectWrapper = styled.div``;

export const SelectStyled = styled.label`
  user-select: none;
`;

export const ActualSelectStyled = styled(Select)`
  min-width: 150px;
`;

export const InputErrors = styled(motion.div)`
  margin: 1rem 0;
  p {
    color: ${colorRed};
  }
`;
