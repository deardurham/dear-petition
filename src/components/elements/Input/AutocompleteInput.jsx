import React, { useState } from 'react';
import Autosuggest from 'react-autosuggest';

import { Badge, AutoCompleteBadge } from '../Badge/Badge';
import AutoSuggestInput from '../AutoSuggest/AutoSuggestInput';
import AutoSuggestionContainer from '../AutoSuggest/AutoSuggestionContainer';
import useDebounce from '../../../hooks/useDebounce';

const MAX_SUGGESTIONS = 5;

const renderSuggestion = (suggestion, { isHighlighted }) => (
  <AutoCompleteBadge name={suggestion} isHighlighted={isHighlighted} />
);

const renderAutoSuggestInput = (inputProps, label) => (
  <div className="flex flex-col w-[200px] items-start">
    <AutoSuggestInput label={label} innerClassName="p-2" {...inputProps} type="search" />
  </div>
);

const AutocompleteInput = ({
  selections,
  onSelect,
  onRemoveSelection,
  fetchSuggestions,
  highlightFirstSuggestion,
  label,
}) => {
  const [suggestions, setSuggestions] = useState([]);
  const [suggestionValue, setSuggestionValue] = useState('');
  const debounceFetchSuggestions = useDebounce(
    async (value) => {
      const newSuggestions = ((await fetchSuggestions(value)) ?? [])
        .filter((suggestion) => !selections.includes(suggestion))
        .slice(0, MAX_SUGGESTIONS);
      setSuggestions(newSuggestions);
    },
    {
      timeout: 300,
    }
  );

  const handleSuggestionChange = (_, { newValue }) => {
    setSuggestionValue(newValue);
  };

  const handleSuggestionSelected = (_, { suggestion }) => {
    setSuggestionValue('');
    onSelect(suggestion);
  };

  const handleSuggestionFetch = ({ value }) => {
    debounceFetchSuggestions(value);
  };

  const inputProps = {
    value: suggestionValue,
    onChange: handleSuggestionChange,
  };
  return (
    <div>
      <Autosuggest
        suggestions={suggestions}
        onSuggestionsFetchRequested={handleSuggestionFetch}
        onSuggestionsClearRequested={() => setSuggestions([])}
        getSuggestionValue={(suggestion) => suggestion.name}
        renderSuggestion={renderSuggestion}
        inputProps={inputProps}
        onSuggestionSelected={handleSuggestionSelected}
        highlightFirstSuggestion={highlightFirstSuggestion ?? false}
        renderInputComponent={(autoSuggestInputProps) =>
          renderAutoSuggestInput(autoSuggestInputProps, label)
        }
        renderSuggestionsContainer={(props) => <AutoSuggestionContainer {...props} />}
      />
      <div className="flex flex-wrap select-none">
        {selections.map((selection, i) => (
          <Badge
            key={`${i}_${selection}`}
            name={selection}
            remove={() => onRemoveSelection(selection)}
          />
        ))}
      </div>
    </div>
  );
};

export default AutocompleteInput;
