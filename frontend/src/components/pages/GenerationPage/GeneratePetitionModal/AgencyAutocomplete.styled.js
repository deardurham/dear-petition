import styled from 'styled-components';
import { colorBlack } from '../../../../styles/colors';

const AgencyAutocompleteStyled = styled.div`
  width: 100%;
  padding: 1rem 2rem;
  border-bottom: 1px solid ${colorBlack};
`;

const BadgesListStyled = styled.div`
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  margin: 1rem 0;
`;

export { AgencyAutocompleteStyled, BadgesListStyled };
