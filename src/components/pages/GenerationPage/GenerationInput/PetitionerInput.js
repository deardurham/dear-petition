import React from 'react';
import styled from 'styled-components';
import Input from '../../../elements/Input/Input';
import Select from '../../../elements/Input/Select';
import AddressInput from './AddressInput';
import US_STATES from '../../../../constants/US_STATES';

const Row = styled.div`
  display: flex;
  & > div {
    flex: 1;
  }
  & > div:not(:last-child) {
    margin-right: 1rem;
  }
`;

export default function PetitionerInput({
  petitionerData,
  setPetitionerData,
  errors,
  onClearError
}) {
  const { name, ssn, licenseNumber, licenseState, ...address } = petitionerData;
  const handleChange = (key, value) => {
    setPetitionerData(prev => ({ ...prev, [key]: value }));
    onClearError(key);
  };
  return (
    <>
      <Row>
        <Input
          label="Name"
          value={name}
          onChange={e => handleChange('name', e.target.value)}
          errors={errors.name}
        />
        <Input
          label="SSN"
          value={ssn}
          maxLength={11}
          onChange={e => handleChange('ssn', e.target.value.replace(/[^0-9-]/g, ''))}
          errors={errors.ssn}
        />
      </Row>
      <Row>
        <Input
          label="License #"
          value={licenseNumber}
          onChange={e => handleChange('licenseNumber', e.target.value)}
          errors={errors.licenseNumber}
        />
        <Select
          label="License state"
          value={licenseState}
          onChange={value => handleChange('licenseState', value)}
          options={US_STATES.map(state => ({ value: state[0], label: state[0] }))}
          errors={errors.licenseState}
        />
      </Row>
      <AddressInput
        address={address}
        setAddress={setPetitionerData}
        errors={errors}
        onClearError={onClearError}
      />
    </>
  );
}