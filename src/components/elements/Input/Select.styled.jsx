import styled from 'styled-components';
import Select from 'react-select';
import { motion } from 'framer-motion';
import { colorGrey, colorRed } from '../../../styles/colors';

export const SelectWrapper = styled.div``;

export const SelectStyled = styled.label`
  user-select: none;
  font-size: 1.4rem;
`;

export const ActualSelectStyled = styled(Select)`
  min-width: 150px;
  font-size: 1.5rem;
  & > div {
    border: 1px solid ${colorGrey};
    border-radius: 5px;
  }
  & > div > * {
    border: none;
  }
`;

export const InputErrors = styled(motion.div)`
  margin: 1rem 0;
  user-select: none;
  & p {
    color: ${colorRed};
  }
`;
