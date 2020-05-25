import React from 'react';
import styled from 'styled-components';
import { colorGrey } from '../../../styles/colors'

const AutoSuggestInput = inputProps => {
    return (
        <AutoSuggestInputStyled>
            <InputStyled {...inputProps} />
        </AutoSuggestInputStyled>
    );
};

const AutoSuggestInputStyled = styled.div`
`;

const InputStyled = styled.input`
  width: 100%;
  border: 2px solid ${colorGrey};
  padding: 1rem 2rem;
`;

export default AutoSuggestInput;
