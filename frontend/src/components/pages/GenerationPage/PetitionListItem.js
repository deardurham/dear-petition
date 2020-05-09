import React from 'react';
import { PetitionListItemStyled, PetitionCellStyled } from './PetitionListItem.styled';

function PetitionListItem({ petition }) {
    return (
        <PetitionListItemStyled>
            <PetitionCellStyled>{petition.type}</PetitionCellStyled>
            <PetitionCellStyled>{petition.county}</PetitionCellStyled>
            <PetitionCellStyled>{petition.court}</PetitionCellStyled>
        </PetitionListItemStyled>
    );
}

export default PetitionListItem;
