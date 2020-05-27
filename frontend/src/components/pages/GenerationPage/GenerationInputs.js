import React, { useState, useEffect, useContext } from 'react';
import { GenerationInputsStyled, GenerationInputWrapper } from './GenerationInputs.styled';
import Input from '../../elements/Input/Input';
import Select from '../../elements/Input/Select';
import { GenerationContext } from './GenerationPage';

const FAKE_ATTORNEYS = [
  { id: 0, name: 'Jeff' },
  { id: 1, name: 'Madge' }
];

function GenerationInputs(props) {
  const { attorney, ssn, license, setAttorney, setSSN, setLicense } = useContext(GenerationContext);

  useEffect(() => {
    // fetch attornies
  });

  const mapAttorneysToOptions = () => {
    return FAKE_ATTORNEYS.map(att => ({ value: att.id, label: att.name }));
  };

  return (
    <GenerationInputsStyled>
      <GenerationInputWrapper>
        <Select
          label="Attorney"
          value={attorney}
          onChange={val => setAttorney(val)}
          options={mapAttorneysToOptions()}
        />
      </GenerationInputWrapper>

      <GenerationInputWrapper>
        <Input
          label="SSN"
          value={ssn}
          onChange={e => setSSN(e.target.value)}
          maxLength={11} // in case they want to add dashes?
        />
      </GenerationInputWrapper>

      <GenerationInputWrapper>
        <Input label="License #" value={license} onChange={e => setLicense(e.target.value)} />
      </GenerationInputWrapper>
    </GenerationInputsStyled>
  );
}

export default GenerationInputs;
