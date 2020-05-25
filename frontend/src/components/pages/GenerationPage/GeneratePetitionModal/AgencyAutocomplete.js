import React, { useState } from 'react';
import styled from 'styled-components';

// Deps
import Autosuggest from 'react-autosuggest';

// Components
import { AgencyAutocompleteStyled, BadgesListStyled } from './AgencyAutocomplete.styled';
import { Badge, AutoCompleteBadge } from '../../../elements/Badge/Badge';
import AutoSuggestInput from '../../../elements/AutoSuggest/AutoSuggestInput';
import AutoSuggestionContainer from '../../../elements/AutoSuggest/AutoSuggestionContainer';

const renderSuggestion = (suggestion, { isHighlighted }) => {
    return (
        <SuggestionStyled>
            <AutoCompleteBadge {...suggestion} isHighlighted={isHighlighted} />
        </SuggestionStyled>
    );
};

const AgencyAutocomplete = ({ ...props }) => {
    const [suggestions, setSuggestions] = useState([]);
    const [suggestionValue, setSuggestionValue] = useState('');
    const [selectedAgencies, setSelectedAgncies] = useState([]);

    const searchAgencies = [
        {
            "pk": 3,
            "name": "Durham County Sheriff’s Office",
            "category": "agency",
            "address1": "602 E. Main St.",
            "address2": "Durham, NC 27701",
            "city": "",
            "state": "",
            "zipcode": ""
        },
        {
            "pk": 4,
            "name": "Durham Police Department",
            "category": "agency",
            "address1": "510 S. Dillard St.",
            "address2": "Durham, NC 27701",
            "city": "",
            "state": "",
            "zipcode": ""
        },
        {
            "pk": 5,
            "name": "Wake County Sheriff’s Office",
            "category": "agency",
            "address1": "330 S. Salisbury St.",
            "address2": "Raleigh, NC 27601",
            "city": "",
            "state": "",
            "zipcode": ""
        },
        {
            "pk": 6,
            "name": "Raleigh Police Department",
            "category": "agency",
            "address1": "6716 Six Forks Rd.",
            "address2": "Raleigh, NC 27615",
            "city": "",
            "state": "",
            "zipcode": ""
        },
        {
            "pk": 7,
            "name": "Orange County Sheriff",
            "category": "agency",
            "address1": "106 E Margaret Ln",
            "address2": "Hillsborough, NC 27278",
            "city": "",
            "state": "",
            "zipcode": ""
        },
        {
            "pk": 8,
            "name": "Orange County Police Department",
            "category": "agency",
            "address1": "127 N Churton St.",
            "address2": "Hillsborough, NC 27278",
            "city": "",
            "state": "",
            "zipcode": ""
        },
    ]

    const handleHotKeyPressed = e => {
        e.stopPropagation();
        if (e.key === 'Backspace' && e.shiftKey) removeAgency();
    };

    const handleSuggestionChange = (_, { newValue }) => {
        setSuggestionValue(newValue);
    };

    const handleSuggestionsFetchRequested = ({ value }) => {
        setSuggestions(getSuggestions(value));
    };

    const handleSuggestionsClearRequested = () => {
        setSuggestions([]);
    };

    const getSuggestions = value => {
        const inputValue = value.trim().toLowerCase();
        const inputLength = inputValue.length;
        let availableAgencies = [...searchAgencies];
        availableAgencies = availableAgencies.filter(
            thisAgency => !selectedAgencies.map(innerAgency => innerAgency.name).includes(thisAgency.name)
        );
        return inputLength === 0
            ? []
            : availableAgencies.filter(
                thisAgency => thisAgency.name.toLowerCase().slice(0, inputLength) === inputValue
            );
    };

    const handleSuggestionSelected = (_, { suggestion }) => {
        addAgency(suggestion);
    };

    const addAgency = thisAgency => {
        console.log(thisAgency);
        setSuggestionValue('');
        setSelectedAgncies([...selectedAgencies, thisAgency]);

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
        setSelectedAgncies(theseAgencies);
    };

    const inputProps = {
        value: suggestionValue,
        onChange: handleSuggestionChange,
        onKeyUp: handleHotKeyPressed
    };

    return (
        <AgencyAutocompleteStyled {...props} data-cy="agency_autocomplete">
            <h3>Agencies</h3>
            <Autosuggest
                suggestions={suggestions}
                onSuggestionsFetchRequested={handleSuggestionsFetchRequested}
                onSuggestionsClearRequested={handleSuggestionsClearRequested}
                getSuggestionValue={suggestion => suggestion.name}
                renderSuggestion={renderSuggestion}
                inputProps={inputProps}
                onSuggestionSelected={handleSuggestionSelected}
                highlightFirstSuggestion
                renderInputComponent={AutoSuggestInput}
                renderSuggestionsContainer={AutoSuggestionContainer}
            />
            <BadgesListStyled data-cy="label_list">
                {selectedAgencies.map((thisAgency, i) => (
                    <Badge
                        {...thisAgency}
                        key={`${i}_${thisAgency.name}`}
                        remove={() => removeAgency(thisAgency)}
                        data-cy="label_item"
                    />
                ))}
            </BadgesListStyled>
        </AgencyAutocompleteStyled>
    );
};

const SuggestionStyled = styled.div``;

export default AgencyAutocomplete;
