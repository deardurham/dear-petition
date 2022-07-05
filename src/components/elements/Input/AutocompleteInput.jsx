import React, { useState } from 'react';
import cx from 'classnames';
import Autosuggest from 'react-autosuggest';

import { Badge } from '../Badge/Badge';
import AutoSuggestInput from '../AutoSuggest/AutoSuggestInput';
import useDebounce from '../../../hooks/useDebounce';

const MAX_SUGGESTIONS = 5;

const Suggestion = ({ isHighlighted, name }) => (
  <div
    className={cx(
      'flex items-center justify-between gap-3 rounded-md bg-white px-2 py-1',
      'bg-white text-gray-900 cursor-pointer',
      {
        'outline outline-2 outline-yellow-400': isHighlighted,
      }
    )}
  >
    <p className="text-lg text-inherit">{name}</p>
  </div>
);

const SuggestionContainer = ({ containerProps: { className, ...restProps }, children }) => (
  <div
    className={cx(
      className,
      { 'border border-gray-800 rounded-md': !!children },
      '[&>ul]:divide-gray-800 [&>ul]:divide-y w-full'
    )}
    {...restProps}
  >
    {children}
  </div>
);

const renderSuggestion = (suggestion, { isHighlighted }) => (
  <Suggestion name={suggestion} isHighlighted={isHighlighted} />
);

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
  getSuggestionLabel,
}) => {
  const [suggestions, setSuggestions] = useState([]);
  const [suggestionValue, setSuggestionValue] = useState('');
  const debounceFetchSuggestions = useDebounce(
    async (value) => {
      const newSuggestions = ((await fetchSuggestions(value)) ?? []).slice(0, MAX_SUGGESTIONS);
      setSuggestions(newSuggestions);
    },
    {
      timeout: 300,
    }
  );

  const handleSuggestionChange = (_event, { newValue, method }) => {
    if (method === 'type' || method === 'enter') {
      setSuggestionValue(newValue);
    }
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
    onBlur: () => setSuggestions([]),
  };
  return (
    <div className="flex flex-col w-[300px]">
      <Autosuggest
        suggestions={suggestions}
        onSuggestionsFetchRequested={handleSuggestionFetch}
        onSuggestionsClearRequested={() => setSuggestions([])}
        getSuggestionValue={(suggestion) => suggestion.name}
        renderSuggestion={(suggestion, params) =>
          renderSuggestion(getSuggestionLabel ? getSuggestionLabel(suggestion) : suggestion, params)
        }
        inputProps={inputProps}
        onSuggestionSelected={handleSuggestionSelected}
        highlightFirstSuggestion={highlightFirstSuggestion ?? false}
        renderInputComponent={(autoSuggestInputProps) =>
          renderAutoSuggestInput(autoSuggestInputProps, label)
        }
        renderSuggestionsContainer={(props) => <SuggestionContainer {...props} />}
      />
      <div className="flex flex-wrap max-h-[70px] mt-2 overflow-auto gap-2 select-none">
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
