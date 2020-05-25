import React, { useContext } from 'react';
import styled from 'styled-components';
import { ModalStyled, ModalContent } from '../HomePage/HomePage.styled'
import { GenerationContext } from './GenerationPage';
import useKeyPress from '../../../hooks/useKeyPress';

const GeneratePetitionModal = ({ closeModal, isVisible }) => {
    const { petition } = useContext(GenerationContext);

    useKeyPress('Escape', closeModal);

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
