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
  display: flex;
  padding: 2rem;
  margin: 0;
`;

export const PetitionListHeader = styled(PetitionListRow)`
  font-weight: bold;
`;

export const PetitionListItemStyled = styled(PetitionListRow)`
  cursor: pointer;

  &:nth-child(even) {
    background-color: ${greyScale(9.5)};
  }

  &:hover {
    background: ${greyScale(8)};
  }
  padding: 2rem;
`;

export const PetitionCellStyled = styled.div`
  flex: 1;
`;

export const GenerateButtonCell = styled(PetitionCellStyled)`
  flex: 0;
`;
