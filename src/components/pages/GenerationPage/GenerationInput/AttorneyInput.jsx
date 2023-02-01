import React from 'react';
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

export default function AttorneyInput({ attorney, setAttorney, errors, onClearError }) {
  const [triggerSuggestionsFetch] = useLazySearchAttorniesQuery();
  const { address1, address2, city, state, zipcode } = attorney;

  return (
    <div className="mt-2">
      <AutocompleteInput
        placeholder="Search for an attorney..."
        selections={attorney}
        onSelect={(attorneyResult) => {
          setAttorney(attorneyResult);
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
          <AddressInput address={{ address1, address2, city, state, zipcode }} disabled />
        </div>
      )}
    </div>
  );
}
