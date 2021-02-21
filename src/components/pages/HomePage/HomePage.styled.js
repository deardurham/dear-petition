import styled from 'styled-components';
import { smallerThanTabletLandscape } from '../../../styles/media';
import { colorWhite, colorWarning, colorCaution } from '../../../styles/colors';

// Base
import PageBase from '../PageBase';
import Modal from '../../elements/Modal/Modal';

export const HomePageStyled = styled(PageBase)`
  section {
    justify-content: center;
  }
`;

export const HomeContent = styled.div`
  display: flex;
  flex: 1;
  margin-top: 1rem;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  }
`;

export const DnDContent = styled.div`
  height: 420px;
  width: 350px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;

  & > div {
    margin-top: 5rem;
  }
`;

export const DragWarnings = styled.div`
  p {
    color: ${colorWarning};
    padding: 1rem 1rem 0 1rem;
  }
`;

export const DragErrors = styled.div`
  p {
    color: ${colorCaution};
    padding: 1rem 1rem 0 1rem;
  }
`;

export const ModalStyled = styled(Modal)`
  position: absolute;
  bottom: 50%;
  left: 50%;
  transform: translate(-50%, 50%);
`;

export const ModalContent = styled.div`
  background-color: ${colorWhite};
  width: 500px;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
`;
