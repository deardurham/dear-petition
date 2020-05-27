import styled from 'styled-components';
import { colorWhite } from '../../../../styles/colors';

export const ModalContent = styled.div`
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
