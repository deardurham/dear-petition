import React, { useState } from 'react';
import { PetitionListItemStyled, PetitionCellStyled } from './PetitionListItem.styled';
import GeneratePetitionModal from './GeneratePetitionModal/GeneratePetitionModal';

function PetitionListItem({ petition, selectPetition }) {
  const [isVisible, setIsVisible] = useState(false);
  return (
    <>
      <PetitionListItemStyled onClick={() => { selectPetition(); setIsVisible(true); } }>
        <PetitionCellStyled>{petition.form_type}</PetitionCellStyled>
        <PetitionCellStyled>{petition.county} County</PetitionCellStyled>
        <PetitionCellStyled>{petition.jurisdiction}</PetitionCellStyled>
      </PetitionListItemStyled>
      {isVisible && (
        <GeneratePetitionModal isVisible={isVisible} closeModal={() => setIsVisible(false)}/>
      )}
    </>
  );
}

export default PetitionListItem;
