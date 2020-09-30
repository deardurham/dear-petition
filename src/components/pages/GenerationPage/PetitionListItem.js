import React, { useState } from 'react';
import { PetitionListItemStyled, PetitionCellStyled } from './PetitionListItem.styled';
import GeneratePetitionModal from './GeneratePetitionModal/GeneratePetitionModal';

function PetitionListItem({ petition, validatePetitionSelect }) {
  const [isVisible, setVisible] = useState(false);
  const handleClick = () => {
    if (validatePetitionSelect(petition)) {
      setVisible(true);
    }
  };
  return (
    <>
      <PetitionListItemStyled onClick={handleClick}>
        <PetitionCellStyled>{petition.form_type}</PetitionCellStyled>
        <PetitionCellStyled>{petition.county} County</PetitionCellStyled>
        <PetitionCellStyled>{petition.jurisdiction}</PetitionCellStyled>
      </PetitionListItemStyled>
      {isVisible && (
        <GeneratePetitionModal
          isVisible={isVisible}
          closeModal={() => setVisible(false)}/>
      )}
    </>
  );
}

export default PetitionListItem;
