import styled from 'styled-components';
import { colorGrey, colorRed, colorFontPrimary } from '../../../styles/colors';
import { motion } from 'framer-motion';
import { fontPrimary } from '../../../styles/fonts';

export const InputWrapper = styled.div``;

export const InputStyled = styled.label`
  user-select: none;
`;

export const ActualInputStyled = styled.input`
  display: block;
  border-radius: 5px;
  padding: 1rem 2rem;

  width: 100%;
  border: 1px solid ${colorGrey};
  font-size: 16px;
  font-family: ${fontPrimary};
  color: ${colorFontPrimary};
`;

export const InputErrors = styled(motion.div)`
  margin: 1rem 0;
  p {
    color: ${colorRed};
  }
`;
