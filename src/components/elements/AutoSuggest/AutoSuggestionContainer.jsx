import React from 'react';
import styled from 'styled-components';
import { colorWhite, colorBlack } from '../../../styles/colors';
import keyAndAmbientShadows from '../../../styles/shadows';

const AutoSuggestionContainer = ({ containerProps, children }) => (
  <AutoSuggestionContainerStyled {...containerProps}>{children}</AutoSuggestionContainerStyled>
);

const AutoSuggestionContainerStyled = styled.div`
  position: absolute;
  z-index: 10;
  min-width: 13rem;
  display: flex;
  flex-direction: column;

  border-radius: 10px;
  background-color: ${colorWhite};
  box-shadow: ${keyAndAmbientShadows.dp6};

  & p {
    margin: 1rem 0;
    white-space: nowrap;
    padding: 0 1.5rem;
    font-size: 1.5rem;
    color: ${colorBlack};
  }
`;

export default AutoSuggestionContainer;
