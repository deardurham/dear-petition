import React, { useContext } from 'react';
import styled from 'styled-components';
import { ModalStyled, ModalContent } from '../HomePage/HomePage.styled'
import { GenerationContext } from './GenerationPage';

const GeneratePetitionModal = ({ closeModal, isVisible }) => {
    const { petition } = useContext(GenerationContext);

    return (
        <GeneratePetitionModalStyled isVisible={isVisible}>
            <ModalContent>
                {petition ? (
                    <>
                        <h2>{petition.type}</h2>
                        <div onClick={closeModal}>Close</div>
                    </>
                ) : ''}
            </ModalContent>
        </GeneratePetitionModalStyled>
    );
};

const GeneratePetitionModalStyled = styled(ModalStyled)``;

export default GeneratePetitionModal;
