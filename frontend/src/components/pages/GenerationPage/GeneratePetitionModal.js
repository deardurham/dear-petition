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
                        <ul>
                            <li>Jurisdiction: {petition.court}</li>
                            <li>County: {petition.county} County</li>
                        </ul>
                        <div onClick={closeModal}>Close</div>
                    </>
                ) : ''}
            </ModalContent>
        </GeneratePetitionModalStyled>
    );
};

const GeneratePetitionModalStyled = styled(ModalStyled)``;

export default GeneratePetitionModal;
