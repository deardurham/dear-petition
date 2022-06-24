import React, { useState } from 'react';
import Autosuggest from 'react-autosuggest';

import { Badge } from '../Badge/Badge';
import AutoSuggestInput from '../AutoSuggest/AutoSuggestInput';
import AutoSuggestionContainer from '../AutoSuggest/AutoSuggestionContainer';
import useDebounce from '../../../hooks/useDebounce';

const MAX_SUGGESTIONS = 5;

const renderSuggestion = (suggestion) => <Badge name={suggestion} />;

const renderAutoSuggestInput = (inputProps, label) => (
  <div className="flex flex-col w-[250px] items-start mb-1">
    <AutoSuggestInput
      label={label}
      innerClassName="w-full p-2"
      {...inputProps}
      className="w-[250px]"
      type="search"
    />
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
    <div className="flex flex-col w-[300px]">
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
      <div className="flex flex-wrap max-h-[70px] overflow-auto gap-2 select-none">
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
