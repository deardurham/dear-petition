import React from 'react';
import styled from 'styled-components';
import Input from '../../../elements/Input/Input';
import AddressInput from './AddressInput';

const TextInput = styled(Input)`
  input {
    padding: 0.9rem;
    width: 100%;
  }
  &:not(:last-child) {
    margin-bottom: 1rem;
  }
`;

export default function PetitionerInput({
  petitionerData,
  setPetitionerData,
  errors,
  onClearError,
}) {
  const { name, ...address } = petitionerData;
  const handleChange = (key, value) => {
    setPetitionerData((prev) => ({ ...prev, [key]: value }));
    onClearError(key);
  };
  return (
    <>
      <TextInput
        label="Name"
        value={name}
        onChange={(e) => handleChange('name', e.target.value)}
        errors={errors.name}
      />
      <AddressInput
        address={address}
        setAddress={setPetitionerData}
        errors={errors}
        onClearError={onClearError}
      />
    </>
  );
}
