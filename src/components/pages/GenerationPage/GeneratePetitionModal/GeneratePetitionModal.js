import React, { useContext } from 'react';
import styled from 'styled-components';
import { ModalStyled } from '../../HomePage/HomePage.styled';
import { ModalContent } from './GeneratePetitionModal.styled';

// Hooks
import useKeyPress from '../../../../hooks/useKeyPress';

// Children/Components
import AgencyAutocomplete from './AgencyAutocomplete';
import { GenerationContext } from '../GenerationPage';
import Button from '../../../elements/Button/Button';
import Axios from '../../../../service/axios';

const GeneratePetitionModal = ({ closeModal, isVisible }) => {
  const { petition, ssn, licenseNumber, licenseState, attorney, selectedAgencies } = useContext(
    GenerationContext
  );

  useKeyPress('Escape', closeModal);

  const _buildPetition = () => {
    return {
      petition: petition.pk,
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

    const pdfBlobUrl = window.URL.createObjectURL(pdfBlob);
    window.open(pdfBlobUrl);

    setTimeout(function() {
      // For Firefox it is necessary to delay revoking the ObjectURL
      window.URL.revokeObjectURL(pdfBlobUrl);
    }, 100);
  };

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
