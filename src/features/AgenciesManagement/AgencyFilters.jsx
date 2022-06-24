import React from 'react';

import { useLazyGetContactFilterOptionsQuery } from '../../service/api';
import { useModalContext } from '../../components/elements/Button/ModalButton';
import { Button } from '../../components/elements/Button';
import AutocompleteInput from '../../components/elements/Input/AutocompleteInput';

export const AgencyFiltersModal = ({ onFilter, filterSelections }) => {
  const { closeModal } = useModalContext();
  return (
    <div className="w-[500px] h-[400px] flex flex-col justify-center items-center gap-4">
      <h2 className="self-center">Filters</h2>
      <AgencyFilters onFilter={onFilter} filterSelections={filterSelections} />
      <Button colorClass="neutral" className="self-center w-max mt-4" onClick={() => closeModal()}>
        Close
      </Button>
    </div>
  );
};

const ContactFilter = ({ field, category, label, onFilter, filterSelections }) => {
  const [triggerSuggestionsFetch] = useLazyGetContactFilterOptionsQuery();
  const addSelection = (value) => {
    onFilter(field, [...filterSelections, value]);
  };
  const removeSelection = (value) => {
    onFilter(
      field,
      filterSelections.filter((element) => element !== value)
    );
  };
  return (
    <AutocompleteInput
      label={label}
      selections={filterSelections}
      onSelect={(value) => addSelection(value)}
      onRemoveSelection={(value) => removeSelection(value)}
      fetchSuggestions={async (searchValue) => {
        const data = await triggerSuggestionsFetch(
          {
            params: { field, category, search: searchValue },
          },
          true
        ).unwrap();
        return data;
      }}
    />
  );
};

const AgencyContactFilter = ({ field, label, onFilter, filterSelections }) => (
  <ContactFilter
    field={field}
    category="agency"
    label={label}
    onFilter={onFilter}
    filterSelections={filterSelections}
  />
);

const AgencyFilters = ({ onFilter, filterSelections }) => (
  <>
    <AgencyContactFilter
      field="city"
      label="City"
      onFilter={onFilter}
      filterSelections={filterSelections.city}
    />
    <AgencyContactFilter
      field="zipcode"
      label="Zip"
      onFilter={onFilter}
      filterSelections={filterSelections.zipcode}
    />
  </>
);
