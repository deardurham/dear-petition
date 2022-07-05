import React, { useState } from 'react';
import styled from 'styled-components';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTimes } from '@fortawesome/free-solid-svg-icons';

// Hooks
import useKeyPress from '../../../../hooks/useKeyPress';

import Modal from '../../../elements/Modal/Modal';
import { Button, CloseButton } from '../../../elements/Button';
import Axios from '../../../../service/axios';
import { useLazyAgenciesQuery } from '../../../../service/api';
import AutocompleteInput from '../../../elements/Input/AutocompleteInput';

const ModalCloseButton = styled(CloseButton)`
  position: absolute;
  top: 0;
  right: 0;
`;

const ModalStyled = styled(Modal)`
  width: 500px;

  & > div {
    gap: 1.25rem;
  }

  ul + div {
    padding: 0;
  }
  button {
    font-size: 1.6rem;
  }
  div + button {
    align-self: center;
    width: 100px;
    padding: 1rem;
  }
  input {
    padding: 1rem;
  }
`;

const GeneratePetitionModal = ({
  agencies,
  attachmentNumber,
  attorney,
  petition,
  petitionerData,
  onClose,
  setAgencies,
}) => {
  const [pdfWindow, setPdfWindow] = useState({ handle: null, url: null });
  const [error, setError] = useState('');
  // const [generatePetition, { error }] = useGeneratePetitionMutation();
  const [triggerSuggestionsFetch] = useLazyAgenciesQuery();

  const _buildPetition = () => ({
    petition: petition.pk,
    name_petitioner: petitionerData.name,
    address1: petitionerData.address1,
    address2: petitionerData.address2,
    city: petitionerData.city,
    state: petitionerData.state.value,
    zip_code: petitionerData.zipCode,
    attorney: attorney.value,
    agencies: agencies.map((agency) => agency.pk),
  });

  const _openPdf = (pdf) => {
    const pdfBlob = new Blob([pdf], { type: 'application/pdf' });

    // IE doesn't allow using a blob object directly as link href
    // instead it is necessary to use msSaveOrOpenBlob
    if (window.navigator && window.navigator.msSaveOrOpenBlob) {
      window.navigator.msSaveOrOpenBlob(pdfBlob);
      return;
    }

    // Clean up previous pdf when generating new one
    const { handle: oldHandle, url: oldUrl } = pdfWindow;
    if (oldUrl) window.URL.revokeObjectURL(oldUrl);
    if (oldHandle) oldHandle.close();

    const url = window.URL.createObjectURL(pdfBlob);
    setPdfWindow({ handle: window.open(url), url });
  };

  const closePdf = () => {
    const { url, handle } = pdfWindow;
    if (url) window.URL.revokeObjectURL(url);
    if (handle) handle.close();

    setPdfWindow({ handle: null, url: null });
    onClose();
  };

  useKeyPress('Escape', closePdf);

  const handleGenerate = async () => {
    const derivedPetition = _buildPetition();
    try {
      setError('');
      const { data } = await Axios.post('/generate-petition/', derivedPetition, {
        responseType: 'arraybuffer',
      });
      // TODO: Figure out RTK Query non-serializable ArrayBuffer issue?
      // Note: might not be worthwhile because RTK Query expects to handle only serializable response data
      // const data = await generatePetition(derivedPetition).unwrap();
      _openPdf(data);
    } catch (e) {
      setError(!e?.response && e?.message ? e?.message : 'An unexpected error occurred');
    }
  };

  return (
    <ModalStyled isVisible>
      <ModalCloseButton onClick={closePdf}>
        <FontAwesomeIcon icon={faTimes} />
      </ModalCloseButton>
      {petition && (
        <>
          <h2>{petition.form_type}</h2>
          <ul>
            {attachmentNumber && <li>Attachment #: {attachmentNumber}</li>}
            <li>County: {petition.county} County</li>
            <li>Jurisdiction: {petition.jurisdiction}</li>
          </ul>
          <AutocompleteInput
            label="Agencies"
            selections={agencies.map((agencyObject) => agencyObject.name)}
            onSelect={(value) => setAgencies((prev) => [...prev, value])}
            onRemoveSelection={(name) =>
              setAgencies((prev) => prev.filter((agency) => agency.name !== name))
            }
            getSuggestionLabel={(agencySuggestion) => agencySuggestion.name}
            fetchSuggestions={async (searchValue) => {
              const data = await triggerSuggestionsFetch(
                { queryString: `search=${searchValue}` },
                true
              ).unwrap();
              const selectedAgencyNames = agencies.map((agency) => agency.name);
              return data.results.filter((agency) => !selectedAgencyNames.includes(agency.name));
            }}
          />
          <Button onClick={handleGenerate}>Generate</Button>
          {error && <span className="text-red">{`Error: ${error}`}</span>}
        </>
      )}
    </ModalStyled>
  );
};

export default GeneratePetitionModal;
