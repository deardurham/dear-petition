import styled from 'styled-components';
import { colorWarning, colorCaution } from '../../../styles/colors';

// Base
import PageBase from '../PageBase';

export const HomePageStyled = styled(PageBase)``;

export const HomeContent = styled.div`
  margin-top: 4rem;
  display: flex;
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
