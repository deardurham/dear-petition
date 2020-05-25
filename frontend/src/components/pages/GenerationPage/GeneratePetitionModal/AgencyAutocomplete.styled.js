import styled from 'styled-components';
import { colorBlack } from '../../../../styles/colors';

const AgencyAutocompleteStyled = styled.div`
  width: 100%;
  padding: 1rem 0rem 2rem 0rem;
`;

const BadgesListStyled = styled.div`
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  margin: 1rem 0;
`;

const AgencyAutoSuggestInputStyled = styled.div`
  display: flex;
  width: 200px;
  flex-direction: column;
  align-items: flex-start;
`;

const SuggestionStyled = styled.div``;

export { AgencyAutocompleteStyled, AgencyAutoSuggestInputStyled, BadgesListStyled, SuggestionStyled };
