import styled from 'styled-components';
import { colorWhite } from '../../../styles/colors';

export const ModalContent = styled.div`
  display: flex;
  flex-direction: column;
  padding: 2rem;
`;

export const ModalStyled = styled.div`
  z-index: 10;
  position: fixed;
  bottom: 50%;
  left: 50%;
  transform: translate(-50%, 50%);
  background-color: ${colorWhite};
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
`;

export const ModalUnderlay = styled.div`
  top: 0;
  bottom: 0;
  left: 0;
  right: 0%;
  position: fixed;
  background: rgba(0, 0, 0, 0.8);
  z-index: 9;
`;
