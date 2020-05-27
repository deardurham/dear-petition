import React, { useContext } from 'react';
import { PetitionListItemStyled, PetitionCellStyled } from './PetitionListItem.styled';
import { GenerationContext } from './GenerationPage';
import GeneratePetitionModal from './GeneratePetitionModal/GeneratePetitionModal';

function PetitionListItem({ petition }) {
  const { showGenerationModal, setShowGenerationModal, handlePetitionSelect } = useContext(
    GenerationContext
  );

  return (
    <>
      <PetitionListItemStyled onClick={() => handlePetitionSelect(petition)}>
        <PetitionCellStyled>{petition.form_type}</PetitionCellStyled>
        <PetitionCellStyled>{petition.county} County</PetitionCellStyled>
        <PetitionCellStyled>{petition.jurisdiction}</PetitionCellStyled>
      </PetitionListItemStyled>
      <GeneratePetitionModal
        isVisible={showGenerationModal}
        closeModal={() => setShowGenerationModal(false)}
      />
    </>
  );
}

export default PetitionListItem;
