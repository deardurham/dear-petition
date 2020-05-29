import styled from 'styled-components';


export const ModalStyled = styled.div`
    z-index: 10;
`;

export const ModalUnderlay = styled.div`
    top: 0;
    bottom: 0;
    left: 0;
    right: 0%;
    position: absolute;
    background: rgba(0,0,0,.8);
    z-index: 9;
`;
