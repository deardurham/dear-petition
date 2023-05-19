import { useState } from 'react';
import { Button } from '../components/elements/Button';
import StyledDialog from '../components/elements/Modal/Dialog';
import AutocompleteInput from '../components/elements/Input/AutocompleteInput';
import {
  useLazySearchAgenciesQuery,
  useAssignAgenciesToDocumentsMutation,
  usePetitionQuery,
} from '../service/api';
import { Spinner } from '../components/elements/Spinner';
import { Badge } from '../components/elements/Badge/Badge';

const agencyArraysAreEqual = (agencyArr1, agencyArr2) => {
  if (agencyArr1.length !== agencyArr2.length) {
    return false;
  }
  for (let i = 0; i < agencyArr1.length; i++) {
    if (agencyArr1[i].pk !== agencyArr2[i].pk) {
      return false;
    }
  }
  return true;
};

const sortAgencyArrayByPk = ({ pk: pkA }, { pk: pkB }) => {
  if (pkA < pkB) {
    return -1;
  }
  if (pkA > pkB) {
    return 1;
  }
  return 0;
};

export const SelectAgenciesModal = ({ isOpen, onClose, petitionId }) => {
  const { data: petitionData } = usePetitionQuery({ petitionId });

  const content = petitionData ? (
    <SelectAgencies
      petitionId={petitionId}
      selectedAgencies={petitionData.agencies}
      onClose={onClose}
    />
  ) : (
    <Spinner />
  );

  return (
    <StyledDialog isOpen={isOpen} onClose={() => onClose()}>
      <div className="h-auto flex justify-center">{content}</div>
    </StyledDialog>
  );
};

const SelectAgencies = ({ selectedAgencies, onClose, petitionId }) => {
  const [selections, setSelections] = useState(selectedAgencies);
  const [triggerSuggestionsFetch] = useLazySearchAgenciesQuery();
  const [triggerAssignAgenciesToDocuments] = useAssignAgenciesToDocumentsMutation();

  return (
    <div className="flex flex-col gap-8 w-[600px] p-10">
      <h3>View / Select Agencies</h3>
      <p className="text-[1.6rem]">
        Please select or de-select agencies here if you wish to include or exclude them from the
        petition.
      </p>
      <div>
        <AutocompleteInput
          placeholder="Search for an agency..."
          selections={selections}
          showSelections
          onSelect={(agency) =>
            setSelections((prev) => [...prev, agency].sort(sortAgencyArrayByPk))
          }
          onRemoveSelection={(agency) =>
            setSelections((prev) => prev.filter((a) => a.pk !== agency.pk))
          }
          getSuggestionLabel={({ name }) => name}
          fetchSuggestions={async (searchValue) => {
            const data = await triggerSuggestionsFetch(
              {
                search: searchValue,
              },
              true
            ).unwrap();
            return data.results.filter(
              (suggestion) => !selections.map(({ pk }) => pk).includes(suggestion.pk)
            );
          }}
        />
        <div className="flex flex-wrap max-h-[70px] mt-2 overflow-auto gap-2 select-none">
          {selections.map((selection, i) => (
            <Badge
              key={`${i}_${selection.name}`}
              name={selection.name}
              remove={() => setSelections((prev) => prev.filter((a) => a.pk !== selection.pk))}
            />
          ))}
        </div>
      </div>
      <div className="self-center flex gap-8">
        <Button
          className="px-4"
          disabled={agencyArraysAreEqual(selectedAgencies, selections)}
          title={
            agencyArraysAreEqual(selectedAgencies, selections) &&
            'You must modify the selected agencies to update the petition'
          }
          onClick={() => triggerAssignAgenciesToDocuments({ petitionId, agencies: selections })}
        >
          Update Agencies
        </Button>
        <Button className="px-4" onClick={() => onClose()}>
          Close
        </Button>
      </div>
    </div>
  );
};
