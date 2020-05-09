import React from 'react';
import { GenerationInputsStyled } from './GenerationInputs.styled';
// import { Input } from 'reaktus';

function GenerationInputs(props) {
    return (
        <GenerationInputsStyled>
            <input label="Attorney" />
        </GenerationInputsStyled>
    );
}

export default GenerationInputs;
