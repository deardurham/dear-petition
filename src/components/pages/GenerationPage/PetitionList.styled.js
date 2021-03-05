import styled from 'styled-components';
import { greyScale } from '../../../styles/colors';
import { PetitionList } from './PetitionList';

export const PetitionListStyled = styled(PetitionList)`
  display: flex;
  flex-direction: column;
  border-style: solid;
  border-color: black;
  border-width: 1px;
`;

const PetitionListRow = styled.li`
  margin: 0;
`;

export const PetitionListHeader = styled(PetitionListRow)`
  padding: 2rem;
  font-weight: bold;
  display: flex;
`;

export const PetitionListItemStyled = styled(PetitionListRow)`
  cursor: pointer;

  &:nth-child(even) {
    background-color: ${greyScale(9.5)};
  }
`;

export const PetitionCellStyled = styled.div`
  flex: 1 0 29.2%;
`;

export const GenerateButtonCell = styled(PetitionCellStyled)`
  flex: 0 0 12.5%;
`;
