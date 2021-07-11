import React from 'react';
import Input from '../../../elements/Input/Input';
import AddressInput from './AddressInput';

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
      <Input
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
