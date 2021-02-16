import styled from 'styled-components';
import Input from '../../elements/Input/Input';
import Select from '../../elements/Input/Select';
import { smallerThanTabletLandscape } from '../../../styles/media';

export const FlexWrapper = styled.div`
  display: flex;
  flex-flow: row wrap;

  @media (${smallerThanTabletLandscape}) {
    flex-direction: column;
    justify-content: flex-start;
    align-items: stretch;
  }
`;

export const GenerationInput = styled(Input)`
  width: 25%;
  min-width: 350px;
  margin-top: 1rem;
  margin-right: 4rem;
`;

export const GenerationSelect = styled(Select)`
  width: 25%;
  min-width: 350px;
  margin-top: 1rem;
  margin-right: 4rem;
`;

export const SSN = styled(GenerationInput)`
`;

export const AddressLine = styled(GenerationInput)`
  width: 50%;
`;
