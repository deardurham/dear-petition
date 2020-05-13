import React from 'react';
import { PetitionListItemStyled, PetitionCellStyled } from './PetitionListItem.styled';

function PetitionListItem({ petition }) {
    const handlePetitionSelect = () => {
        // do things
    }
    return (
        <PetitionListItemStyled onClick={handlePetitionSelect}>
            <PetitionCellStyled>{petition.type}</PetitionCellStyled>
            <PetitionCellStyled>{petition.county} County</PetitionCellStyled>
            <PetitionCellStyled>{petition.court} court</PetitionCellStyled>
        </PetitionListItemStyled>
    );
}

export default PetitionListItem;
