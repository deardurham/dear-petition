import React, { useState, useContext } from 'react';
import { PetitionListItemStyled, PetitionCellStyled } from './PetitionListItem.styled';
import { GenerationContext } from './GenerationPage';
import GeneratePetitionModal from './GeneratePetitionModal'

function PetitionListItem({ petition }) {
    const [showModal, setShowModal] = useState(false);
    const { setPetition } = useContext(GenerationContext);

    const handlePetitionSelect = () => {
        setPetition(petition);
        setShowModal(true);
    }
    return (
        <>
            <PetitionListItemStyled onClick={handlePetitionSelect}>
                <PetitionCellStyled>{petition.type}</PetitionCellStyled>
                <PetitionCellStyled>{petition.county} County</PetitionCellStyled>
                <PetitionCellStyled>{petition.court} court</PetitionCellStyled>
            </PetitionListItemStyled>
            <GeneratePetitionModal isVisible={showModal} closeModal={() => setShowModal(false)}></GeneratePetitionModal>
        </>
    );
}

export default PetitionListItem;
