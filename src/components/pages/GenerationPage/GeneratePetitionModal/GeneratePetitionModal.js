import React, { useState } from 'react';
import styled from 'styled-components';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTimes } from '@fortawesome/free-solid-svg-icons';

// Hooks
import useKeyPress from '../../../../hooks/useKeyPress';

import Modal from '../../../elements/Modal/Modal';
import AgencyAutocomplete from '../GenerationInput/AgencyAutocomplete';
import { Button, CloseButton } from '../../../elements/Button';
import Axios from '../../../../service/axios';

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

  ul {
    & > li:not(:last-child) {
      margin-bottom: 0.5rem;
    }
    font-size: 1.6rem;
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
      const { data } = await Axios.post('/generate-petition/', derivedPetition, {
        responseType: 'arraybuffer',
      });
      _openPdf(data);
    } catch (error) {
      // TODO: add error message
      console.error(error);
      console.log(error?.response);
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
          <AgencyAutocomplete agencies={agencies} setAgencies={setAgencies} />
          <Button onClick={handleGenerate}>Generate</Button>
        </>
      )}
    </ModalStyled>
  );
};

export default GeneratePetitionModal;
