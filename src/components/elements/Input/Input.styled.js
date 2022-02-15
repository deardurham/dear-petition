import styled from 'styled-components';
import { colorGrey, colorRed, colorFontPrimary } from '../../../styles/colors';
import { motion } from 'framer-motion';
import { fontPrimary } from '../../../styles/fonts';
import { smallerThanTabletLandscape } from '../../../styles/media';

export const InputWrapper = styled.div``;

export const InputStyled = styled.label`
  user-select: none;
  font-size: 1.4rem;
`;

export const ActualInputStyled = styled.input`
  display: block;
  border-radius: 5px;

  border: 1px solid ${colorGrey};
  font-size: 1.5rem;
  font-family: ${fontPrimary};
  color: ${colorFontPrimary};
`;

export const InputErrors = styled(motion.div)`
  margin-top: 0.5rem;
  p {
    color: ${colorRed};
    @media (${smallerThanTabletLandscape}) {
      font-size: 1.4rem;
    }
  }
`;
