import React from 'react';
import { PetitionListItemStyled } from './PetitionListItem.styled';

function PetitionListItem({ petition }) {
    return (
        <PetitionListItemStyled>
            <p>{petition.type}</p>
        </PetitionListItemStyled>
    );
}

export default PetitionListItem;
