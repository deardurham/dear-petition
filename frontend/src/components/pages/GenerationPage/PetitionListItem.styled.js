import styled from 'styled-components';
import { greyScale } from '../../../styles/colors';

export const PetitionListItemStyled = styled.li`
  display: flex;
  margin: 0 0 2rem 0;
  cursor: pointer;

  &:nth-child(even) {
    background-color: ${greyScale(9.5)};
  }

  &:hover {
    background: ${greyScale(8)};
  }
  margin: 0;
  padding: 2rem;
`;

export const PetitionCellStyled = styled.div`
  display: flex;
  width: 33.33%;
`;
