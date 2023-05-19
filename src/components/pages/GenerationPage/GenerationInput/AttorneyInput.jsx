import styled from 'styled-components';
import AutocompleteInput from '../../../elements/Input/AutocompleteInput';
import { useLazySearchAttorniesQuery } from '../../../../service/api';
import AddressInput from './AddressInput';
import Input from '../../../elements/Input/Input';

const TextInput = styled(Input)`
  input {
    padding: 0.9rem;
    width: 100%;
    background-color: ${(props) => props.disabled && 'hsl(0, 0%, 95%)'};
  }
  &:not(:last-child) {
    margin-bottom: 1rem;
  }
`;

export default function AttorneyInput({ attorney, onSelectAttorney, errors, onClearError }) {
  const [triggerSuggestionsFetch] = useLazySearchAttorniesQuery();

  return (
    <>
      <AutocompleteInput
        placeholder="Search for an attorney..."
        className="w-[250px]"
        onSelect={(attorneyResult) => {
          onSelectAttorney(attorneyResult);
          onClearError('attorney');
        }}
        getSuggestionLabel={({ name }) => name}
        fetchSuggestions={async (searchValue) => {
          const data = await triggerSuggestionsFetch(
            {
              search: searchValue,
            },
            true
          ).unwrap();
          return data.results;
        }}
      />
      {errors?.attorney
        ? errors.attorney.map((errMsg) => (
            <p key={errMsg} className="text-red">
              {errMsg}
            </p>
          ))
        : null}
      {attorney && (
        <div>
          <TextInput label="Name" value={attorney.name} disabled />
          <AddressInput address={attorney} disabled />
        </div>
      )}
    </>
  );
}
