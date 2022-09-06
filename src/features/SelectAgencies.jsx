import React, { useState } from 'react';
import { Button } from '../components/elements/Button';
import StyledDialog from '../components/elements/Modal/Dialog';
import AutocompleteInput from '../components/elements/Input/AutocompleteInput';
import { useParams } from 'react-router-dom';
import {
  useLazySearchAgenciesQuery,
  useAssignAgenciesToDocumentsMutation,
  usePetitionQuery,
} from '../service/api';
import { Spinner } from '../components/elements/Spinner';

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

export const SelectAgenciesModal = ({ isOpen, onClose }) => {
  const { batchId } = useParams();
  const { data: petitionData } = usePetitionQuery({ petitionId: batchId });

  const content = petitionData ? (
    <SelectAgencies selectedAgencies={petitionData.agencies} onClose={onClose} />
  ) : (
    <Spinner />
  );

  return (
    <StyledDialog isOpen={isOpen} onClose={() => onClose()}>
      <div className="h-auto flex justify-center">{content}</div>
    </StyledDialog>
  );
};

const SelectAgencies = ({ selectedAgencies, onClose }) => {
  const { batchId } = useParams();
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
      <AutocompleteInput
        label="Agencies"
        selections={selections}
        onSelect={(agency) => setSelections((prev) => [...prev, agency].sort(sortAgencyArrayByPk))}
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
      <div className="self-center flex gap-8">
        <Button
          className="px-4"
          disabled={agencyArraysAreEqual(selectedAgencies, selections)}
          title="Update the petitions on the main petition row with your changes."
          onClick={() =>
            triggerAssignAgenciesToDocuments({ petitionId: batchId, agencies: selections })
          }
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
