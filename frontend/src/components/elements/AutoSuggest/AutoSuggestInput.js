import React from 'react';
import styled from 'styled-components';
import Input from '../Input/Input';

const AutoSuggestInput = inputProps => {
    return (
        <InputStyled {...inputProps} />
    );
};

const InputStyled = styled(Input)``;

export default AutoSuggestInput;
