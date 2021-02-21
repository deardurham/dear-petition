import React, { useState } from 'react';
import styled from 'styled-components';
import { ModalStyled } from '../../HomePage/HomePage.styled';
import { ModalContent } from './GeneratePetitionModal.styled';

// Hooks
import useKeyPress from '../../../../hooks/useKeyPress';

// Children/Components
import AgencyAutocomplete from './AgencyAutocomplete';
import { Button, CloseButton } from '../../../elements/Button/Button.styled';
import CloseIcon from '../../../elements/Icon/CloseIcon';
import Axios from '../../../../service/axios';

const ModalCloseButton = styled(CloseButton)`
  position: absolute;
  top: 0;
  right: 0;
`;

const GeneratePetitionModal = ({ petition, petitionerData, attorney, onClose }) => {
  const [pdfWindow, setPdfWindow] = useState({ handle: null, url: null});
  const [selectedAgencies, setSelectedAgencies] = useState([]);

  const _buildPetition = () => {
    return {
      petition: petition.pk,
      name_petitioner: petitionerData.petitionerName,
      address1: petitionerData.address.address1,
      address2: petitionerData.address.address2,
      city: petitionerData.address.city,
      state: petitionerData.address.state.value,
      zip_code: petitionerData.address.zipCode,
      ssn: petitionerData.ssn,
      drivers_license: petitionerData.licenseNumber,
      drivers_license_state: petitionerData.licenseState.value,
      attorney: attorney.value,
      agencies: selectedAgencies.map(agency => agency.pk)
    };
  };

  const _openPdf = pdf => {
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
    if (url)
      window.URL.revokeObjectURL(url);
    if (handle)
      handle.close();

    setPdfWindow({ handle: null, url: null });
    onClose();
  };

  useKeyPress('Escape', closePdf);

  const handleGenerate = async () => {
    const derivedPetition = _buildPetition();
    try {
      const { data } = await Axios.post('/generate-petition/', derivedPetition, {
        responseType: 'arraybuffer'
      });
      _openPdf(data);
    } catch (error) {
      console.error(error);
      console.log(error?.response);
    }
  };

  return (
    <GeneratePetitionModalStyled isVisible>
      <ModalContent>
        <ModalCloseButton onClick={closePdf}>
          <CloseIcon />
        </ModalCloseButton>
        {petition && (
          <>
            <h2>{petition.form_type}</h2>
            <ul>
              <li>Jurisdiction: {petition.jurisdiction}</li>
              <li>County: {petition.county} County</li>
            </ul>
            <AgencyAutocomplete selectedAgencies={selectedAgencies} setSelectedAgencies={setSelectedAgencies} />
            <Button onClick={handleGenerate}>Generate</Button>
          </>
        )}
      </ModalContent>
    </GeneratePetitionModalStyled>
  );
};

const GeneratePetitionModalStyled = styled(ModalStyled)``;

export default GeneratePetitionModal;
