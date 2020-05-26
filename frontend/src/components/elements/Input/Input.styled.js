import styled from 'styled-components';
import { colorGrey } from '../../../styles/colors';
import { fontPrimary } from '../../../styles/fonts';

export const InputStyled = styled.label``;

export const ActualInputStyled = styled.input`
  display: block;
  border-radius: 5px;
  padding: 1rem 2rem;
  font-size: 16px;
  font-family: ${fontPrimary};
  border: 1px solid ${colorGrey};

  width: 100%;
  max-width: 300px;
`;
