import styled from 'styled-components';
import { smallerThanTabletLandscape } from '../../../styles/media';

export const GenerationInputsStyled = styled.div`
`;

export const FlexWrapper = styled.div`
  margin: 2rem 0 4rem 0;
  display: flex;
  flex-flow: row wrap;
  justify-content: center;

  @media (${smallerThanTabletLandscape}) {
    flex-direction: column;
    justify-content: flex-start;
    align-items: stretch;
  }
`;

export const GenerationInputWrapper = styled.div`
  margin-right: 4rem;
`;
