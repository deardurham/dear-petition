import styled from 'styled-components';
import { smallerThanTabletLandscape } from '../../../styles/media';

export const GenerationInputsStyled = styled.div`
  margin: 2rem 0 4rem 0;
  display: flex;
  justify-content: center;

  @media (${smallerThanTabletLandscape}) {
    flex-direction: column;
    justify-content: flex-start;
    align-items: stretch;
  }
`;

export const GenerationInputWrapper = styled.div`
  &:not(:first-child) {
    margin-left: 4rem;
  }
`;
