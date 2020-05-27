import React, { useEffect, useContext } from 'react';
import { GenerationInputsStyled, GenerationInputWrapper } from './GenerationInputs.styled';
import Input from '../../elements/Input/Input';
import Select from '../../elements/Input/Select';
import US_STATES from '../../../constants/US_STATES';
import { GenerationContext } from './GenerationPage';

const FAKE_ATTORNEYS = [
  { id: 0, name: 'Jeff' },
  { id: 1, name: 'Madge' }
];

function GenerationInputs() {
  const {
    attorney,
    ssn,
    licenseNumber,
    licenseState,
    setAttorney,
    setSSN,
    setLicenseNumber,
    setLicenseState,
    formErrors
  } = useContext(GenerationContext);

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
          errors={formErrors?.attorney}
        />
      </GenerationInputWrapper>

      <GenerationInputWrapper>
        <Input
          label="SSN"
          value={ssn}
          onChange={e => setSSN(e.target.value)}
          maxLength={11} // in case they want to add dashes?
          errors={formErrors?.ssn}
        />
      </GenerationInputWrapper>

      <GenerationInputWrapper>
        <Input
          label="License #"
          value={licenseNumber}
          onChange={e => setLicenseNumber(e.target.value)}
          errors={formErrors?.licenseNumber}
        />
      </GenerationInputWrapper>

      <GenerationInputWrapper>
        <Select
          label="License state"
          value={licenseState}
          onChange={val => setLicenseState(val)}
          options={US_STATES.map(state => ({ value: state[0], label: state[0] }))}
          errors={formErrors?.licenseState}
        />
      </GenerationInputWrapper>
    </GenerationInputsStyled>
  );
}

export default GenerationInputs;
