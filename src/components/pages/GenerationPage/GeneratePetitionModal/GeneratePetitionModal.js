import React, { useContext, useState } from 'react';
import styled from 'styled-components';
import { ModalStyled } from '../../HomePage/HomePage.styled';
import { ModalContent, CloseButton } from './GeneratePetitionModal.styled';

// Hooks
import useKeyPress from '../../../../hooks/useKeyPress';

// Children/Components
import AgencyAutocomplete from './AgencyAutocomplete';
import { GenerationContext } from '../GenerationPage';
import Button from '../../../elements/Button/Button';
import CloseIcon from '../../../elements/CloseIcon/CloseIcon';
import Axios from '../../../../service/axios';

const GeneratePetitionModal = ({ closeModal, isVisible }) => {
  const { petition, petitionerName, address, ssn, licenseNumber, licenseState, attorney, selectedAgencies } = useContext(
    GenerationContext
  );
  const [pdfWindow, setPdfWindow] = useState({ handle: null, url: null});

  console.log("render");

  const _buildPetition = () => {
    return {
      petition: petition.pk,
      name_petitioner: petitionerName,
      address1: address.address1,
      address2: address.address2,
      city: address.city,
      state: address.state.value,
      zip_code: address.zipCode,
      ssn,
      drivers_license: licenseNumber,
      drivers_license_state: licenseState.value,
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
    setPdfWindow(({ handle, url }) => {
      console.log("CLEAN UP");
      console.log(handle);
      console.log(url);
      if (url)
        window.URL.revokeObjectURL(url);
      if (handle)
        handle.close();
      return { handle: null, url: null };
    });
    closeModal();
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
    <GeneratePetitionModalStyled isVisible={isVisible}>
      <ModalContent>
        <CloseButton onClick={closePdf}>
          <CloseIcon />
        </CloseButton>
        {petition && (
          <>
            <h2>{petition.form_type}</h2>
            <ul>
              <li>Jurisdiction: {petition.jurisdiction}</li>
              <li>County: {petition.county} County</li>
            </ul>
            <AgencyAutocomplete />
            <Button onClick={handleGenerate}>Generate</Button>
          </>
        )}
      </ModalContent>
    </GeneratePetitionModalStyled>
  );
};

const GeneratePetitionModalStyled = styled(ModalStyled)``;

export default GeneratePetitionModal;
