import styled from 'styled-components';
import { colorGrey } from '../../../styles/colors';

import { smallerThanTabletLandscape } from '../../../styles/media';

const GenerationSection = styled.div`
  padding: 2rem 0;
  margin-bottom: 2rem;

  & > h2 {
    user-select: none;
    margin-bottom: 2rem;
  }

  & > p {
    font-size: 1.6rem;
    margin-bottom: 2rem;
  }

  & > div > h3 {
    user-select: none;
    margin-bottom: 1rem;
  }
`;

const InputSectionStyled = styled(GenerationSection)`
  display: flex;
  border-bottom: 1px solid ${colorGrey};

  & > div:first-child {
    flex: 1 0 33%;
  }

  & > div:last-child {
    flex: 1 0 66%;
  }

  @media (${smallerThanTabletLandscape}) {
    flex-flow: column;
  }
`;

const InputSection = ({ children, label }) => (
  <InputSectionStyled>
    <div>
      <h3>{label}</h3>
    </div>
    <div>{children}</div>
  </InputSectionStyled>
);

export default InputSection;
