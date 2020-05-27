import React, { useContext } from 'react';
import styled from 'styled-components';
import { ModalStyled, ModalContent } from '../../HomePage/HomePage.styled';
import { GenerationContext } from '../GenerationPage';
import useKeyPress from '../../../../hooks/useKeyPress';
import AgencyAutocomplete from './AgencyAutocomplete';
import Button from '../../../elements/Button/Button';

const GeneratePetitionModal = ({ closeModal, isVisible }) => {
  const { petition, selectedAgencies } = useContext(GenerationContext);

  useKeyPress('Escape', closeModal);

  const handleGenerate = () => {
    console.log(selectedAgencies);
  };

  return (
    <GeneratePetitionModalStyled isVisible={isVisible} closeModal={closeModal}>
      <ModalContent>
        {petition ? (
          <>
            <h2>{petition.type}</h2>
            <ul>
              <li>Jurisdiction: {petition.court}</li>
              <li>County: {petition.county} County</li>
            </ul>
            <AgencyAutocomplete />
            <Button onClick={handleGenerate}>Generate</Button>
          </>
        ) : (
          ''
        )}
      </ModalContent>
    </GeneratePetitionModalStyled>
  );
};

const GeneratePetitionModalStyled = styled(ModalStyled)``;

export default GeneratePetitionModal;
