import React, { useState, useEffect } from 'react';
import { GenerationInputsStyled, GenerationInputWrapper } from './GenerationInputs.styled';
import Input from '../../elements/Input/Input';
import Select from '../../elements/Input/Select';
import US_STATES from '../../../constants/US_STATES';

const FAKE_ATTORNEYS = [
  { id: 0, name: 'Jeff' },
  { id: 1, name: 'Madge' }
];

function GenerationInputs(props) {
  const [attorney, setAttorney] = useState('');
  const [ssn, setSSN] = useState('');
  const [licenseNumber, setLicenseNumber] = useState('');
  const [licenseState, setLicenseState] = useState('');

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
        <Input
          label="License #"
          value={licenseNumber}
          onChange={e => setLicenseNumber(e.target.value)}
        />
      </GenerationInputWrapper>

      <GenerationInputWrapper>
        <Select
          label="License state"
          value={licenseState}
          onChange={val => setLicenseState(val)}
          options={US_STATES.map(state => ({ value: state[0], label: state[0] }))}
        />
      </GenerationInputWrapper>
    </GenerationInputsStyled>
  );
}

export default GenerationInputs;
