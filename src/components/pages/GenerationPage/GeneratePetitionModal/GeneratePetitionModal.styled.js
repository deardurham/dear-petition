import styled from 'styled-components';
import { colorWhite } from '../../../../styles/colors';
import { keyAndAmbientShadows } from '../../../../styles/shadows';
import Button from '../../../elements/Button/Button';

export const ModalContent = styled.div`
  position: relative;
  background-color: ${colorWhite};
  width: 500px;
  padding: 6rem;
  display: flex;
  flex-direction: column;
  align-items: center;

  h2 {
    margin: 2rem 0;
  }

  ul {
    margin: 1rem;
  }
`;

export const CloseButton = styled(Button)`
  position: absolute;
  right: 0;
  top: 0;
  padding: 0 0.5rem;
  border-radius: 0;
  transition: none;
  transform: none;

  &:hover {
    ${keyAndAmbientShadows.dp2};
    transform: none;
  }

  &:active {
    transform: none;
  }
`;
