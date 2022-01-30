import React, { useState } from 'react';
import styled from 'styled-components';

// Ajax
import Axios from '../../../../service/axios';

// Deps
import Autosuggest from 'react-autosuggest';

// Components
import { Badge, AutoCompleteBadge } from '../../../elements/Badge/Badge';
import AutoSuggestInput from '../../../elements/AutoSuggest/AutoSuggestInput';
import AutoSuggestionContainer from '../../../elements/AutoSuggest/AutoSuggestionContainer';

const AgencyAutocompleteStyled = styled.div`
  width: 100%;
  padding: 1rem 0rem 2rem 0rem;
`;

const BadgesListStyled = styled.div`
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  margin: 1rem 0;
  user-select: none;
`;

const AgencyAutoSuggestInputStyled = styled.div`
  display: flex;
  width: 200px;
  flex-direction: column;
  align-items: flex-start;
`;

const SuggestionStyled = styled.div``;

const renderSuggestion = (suggestion, { isHighlighted }) => (
  <SuggestionStyled>
    <AutoCompleteBadge {...suggestion} isHighlighted={isHighlighted} />
  </SuggestionStyled>
);

const AgencyAutoSuggestInput = (inputProps) => (
  <AgencyAutoSuggestInputStyled>
    <AutoSuggestInput label="Agencies" {...inputProps} />
  </AgencyAutoSuggestInputStyled>
);

const AgencyAutocomplete = ({ agencies, setAgencies, ...props }) => {
  const [suggestions, setSuggestions] = useState([]);
  const [suggestionValue, setSuggestionValue] = useState('');

  const handleHotKeyPressed = (e) => {
    e.stopPropagation();
    if (e.key === 'Backspace' && e.shiftKey) removeAgency();
  };

  const handleSuggestionChange = (_, { newValue }) => {
    setSuggestionValue(newValue);
  };

  const handleSuggestionsFetchRequested = ({ value }) => {
    (async () => {
      try {
        const { data } = await Axios.get(`/contact/?category=agency&search=${value}`);
        const selectedAgencyNames = agencies.map((agency) => agency.name);
        setSuggestions(
          data?.results.filter((agency) => !selectedAgencyNames.includes(agency.name)) || []
        );
      } catch (error) {
        // TODO: add error message
        console.error(error);
      }
    })();
  };

  const handleSuggestionsClearRequested = () => {
    setSuggestions([]);
  };

  const handleSuggestionSelected = (_, { suggestion }) => {
    addAgency(suggestion);
  };

  const addAgency = (thisAgency) => {
    setSuggestionValue('');
    setAgencies((prev) => [...prev, thisAgency]);
  };

  const removeAgency = (thisAgency) => {
    setAgencies((prev) => {
      const theseAgencies = prev.slice();
      if (thisAgency) {
        const { name } = thisAgency;
        const agencyLoc = theseAgencies.map((innerAgency) => innerAgency.name).indexOf(name);
        theseAgencies.splice(agencyLoc, 1);
      } else {
        theseAgencies.pop();
      }
      return theseAgencies;
    });
  };

  const inputProps = {
    value: suggestionValue,
    onChange: handleSuggestionChange,
    onKeyUp: handleHotKeyPressed,
  };

  return (
    <AgencyAutocompleteStyled {...props} data-cy="agency_autocomplete">
      <Autosuggest
        suggestions={suggestions}
        onSuggestionsFetchRequested={handleSuggestionsFetchRequested}
        onSuggestionsClearRequested={handleSuggestionsClearRequested}
        getSuggestionValue={(suggestion) => suggestion.name}
        renderSuggestion={renderSuggestion}
        inputProps={inputProps}
        onSuggestionSelected={handleSuggestionSelected}
        highlightFirstSuggestion
        renderInputComponent={AgencyAutoSuggestInput}
        focusInputOnSuggestionClick={false}
        renderSuggestionsContainer={AutoSuggestionContainer}
      />
      <BadgesListStyled data-cy="label_list">
        {agencies.map((thisAgency, i) => (
          <Badge
            {...thisAgency}
            key={`${i}_${thisAgency.name}`}
            remove={() => removeAgency(thisAgency)}
          />
        ))}
      </BadgesListStyled>
    </AgencyAutocompleteStyled>
  );
};

export default AgencyAutocomplete;
