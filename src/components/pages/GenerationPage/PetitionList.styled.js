import styled from 'styled-components';
import { greyScale } from '../../../styles/colors';
import { PetitionList } from './PetitionList';

export const PetitionListStyled = styled(PetitionList)`
  display: flex;
  flex-direction: column;
  width: 100%;
  border-style: solid;
  border-color: black;
  border-width: 1px;
  margin: 1rem 0rem 0rem 0rem;
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
  display: flex;
  width: 33.33%;
`;
