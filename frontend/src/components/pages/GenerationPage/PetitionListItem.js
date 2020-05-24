import React, { useState, useContext } from 'react';
import { PetitionListItemStyled, PetitionCellStyled } from './PetitionListItem.styled';
import { ModalStyled, ModalContent } from '../HomePage/HomePage.styled'
import { GenerationContext } from './GenerationPage';

function PetitionListItem({ petition }) {
    const [showModal, setShowModal] = useState(false);
    const { batch, setPetition, ssn } = useContext(GenerationContext);

    const handlePetitionSelect = () => {
        setPetition(petition);
        setShowModal(true);
        console.log(ssn)
    }
    return (
        <>
            <PetitionListItemStyled onClick={handlePetitionSelect}>
                <PetitionCellStyled>{petition.type}</PetitionCellStyled>
                <PetitionCellStyled>{petition.county} County</PetitionCellStyled>
                <PetitionCellStyled>{petition.court} court</PetitionCellStyled>
            </PetitionListItemStyled>
            <ModalStyled isVisible={showModal} closeModal={() => setShowModal(false)}>
                <ModalContent>
                    <h2>{petition.type}</h2>
                </ModalContent>
            </ModalStyled>
        </>
    );
}

export default PetitionListItem;
