import styled from 'styled-components';
import Input from '../../elements/Input/Input';
import Select from '../../elements/Input/Select';
import { smallerThanTabletLandscape } from '../../../styles/media';

export const GenerationInput = styled(Input)`
  margin-top: 1rem;
`;

export const GenerationSelect = styled(Select)`
  max-width: 500px;
  margin-top: 1rem;
`;

export const FlexWrapper = styled.div`
  display: flex;
  flex-flow: row wrap;

  & > div:not(:first-child) {
    margin-left: 2rem;
  }

  @media (${smallerThanTabletLandscape}) {
    flex-direction: column;
    justify-content: flex-start;
    align-items: stretch;
    & > div:not(:first-child) {
      margin-left: 0;
    }
  }
`;

export const SSN = styled(GenerationInput)`
  max-width: 400;
`;

export const AddressLine = styled(GenerationInput)`
  max-width: 500px;
`;

export const ZipCode = styled(GenerationInput)`
  max-width: 400px;
`;
