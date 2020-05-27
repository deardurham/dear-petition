import React from 'react';
import { PetitionListItemStyled, PetitionCellStyled } from './PetitionListItem.styled';

function PetitionListItem({ petition }) {
  const handlePetitionSelect = () => {
    // do things
  };
  return (
    <PetitionListItemStyled onClick={handlePetitionSelect}>
      <PetitionCellStyled>{petition.form_type}</PetitionCellStyled>
      <PetitionCellStyled>{petition.county} County</PetitionCellStyled>
      <PetitionCellStyled>{petition.jurisdiction} court</PetitionCellStyled>
    </PetitionListItemStyled>
  );
}

export default PetitionListItem;
