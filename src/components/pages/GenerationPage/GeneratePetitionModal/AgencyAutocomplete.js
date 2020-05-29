import React, { useState, useContext } from 'react';

// Ajax
import Axios from '../../../../service/axios';

// Deps
import Autosuggest from 'react-autosuggest';

// Components
import {
  AgencyAutocompleteStyled,
  BadgesListStyled,
  AgencyAutoSuggestInputStyled,
  SuggestionStyled
} from './AgencyAutocomplete.styled';
import { Badge, AutoCompleteBadge } from '../../../elements/Badge/Badge';
import AutoSuggestInput from '../../../elements/AutoSuggest/AutoSuggestInput';
import AutoSuggestionContainer from '../../../elements/AutoSuggest/AutoSuggestionContainer';
import { GenerationContext } from '../GenerationPage';

const renderSuggestion = (suggestion, { isHighlighted }) => {
  return (
    <SuggestionStyled>
      <AutoCompleteBadge {...suggestion} isHighlighted={isHighlighted} />
    </SuggestionStyled>
  );
};

const AgencyAutoSuggestInput = inputProps => {
  return (
    <AgencyAutoSuggestInputStyled>
      <AutoSuggestInput label="Agencies" {...inputProps} />
    </AgencyAutoSuggestInputStyled>
  );
};

const AgencyAutocomplete = ({ ...props }) => {
  const [suggestions, setSuggestions] = useState([]);
  const [suggestionValue, setSuggestionValue] = useState('');
  const { selectedAgencies, setSelectedAgencies } = useContext(GenerationContext);

  const handleHotKeyPressed = e => {
    e.stopPropagation();
    if (e.key === 'Backspace' && e.shiftKey) removeAgency();
  };

  const handleSuggestionChange = (_, { newValue }) => {
    setSuggestionValue(newValue);
  };

  const handleSuggestionsFetchRequested = ({ value }) => {
    (async function () {
      try {
        const { data } = await Axios.get(`/contact/?category=agency&search=${value}`);
        setSuggestions(data?.results || []);
      } catch (error) {
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

  const addAgency = thisAgency => {
    console.log(thisAgency);
    setSuggestionValue('');
    setSelectedAgencies([...selectedAgencies, thisAgency]);
  };

  const removeAgency = thisAgency => {
    const theseAgencies = selectedAgencies.slice();
    if (thisAgency) {
      const { name } = thisAgency;
      const agencyLoc = selectedAgencies.map(innerAgency => innerAgency.name).indexOf(name);
      theseAgencies.splice(agencyLoc, 1);
    } else {
      theseAgencies.pop();
    }
    setSelectedAgencies(theseAgencies);
  };

  const inputProps = {
    value: suggestionValue,
    onChange: handleSuggestionChange,
    onKeyUp: handleHotKeyPressed
  };

  return (
    <AgencyAutocompleteStyled {...props} data-cy="agency_autocomplete">
      <Autosuggest
        suggestions={suggestions}
        onSuggestionsFetchRequested={handleSuggestionsFetchRequested}
        onSuggestionsClearRequested={handleSuggestionsClearRequested}
        getSuggestionValue={suggestion => suggestion.name}
        renderSuggestion={renderSuggestion}
        inputProps={inputProps}
        onSuggestionSelected={handleSuggestionSelected}
        highlightFirstSuggestion
        renderInputComponent={AgencyAutoSuggestInput}
        renderSuggestionsContainer={AutoSuggestionContainer}
      />
      <BadgesListStyled data-cy="label_list">
        {selectedAgencies.map((thisAgency, i) => (
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
