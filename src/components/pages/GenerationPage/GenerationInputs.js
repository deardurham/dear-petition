import React, { useState, useEffect } from 'react';
import { AddressLine, FlexWrapper, GenerationInput, GenerationSelect } from './GenerationInputs.styled';
// Constants
import US_STATES from '../../../constants/US_STATES';

// Ajax
import Axios from '../../../service/axios';

const AddAgencySelect = ({ agency, setAgencies, disabled, errors }) => (
  <GenerationSelect
    disabled={disabled}
    value={agency}
    onChange={val => {
      console.log(val);
      setAgencies(oldAgencies => [...oldAgencies, val]);
    }}
    options={[{ value: 'Agency 1', label: 'Agency 1' }, { value: 'Agency 2', label: 'Agency 2' }, { value: 'Agency 2', label: 'Agency 3' }]}
    errors={errors}
  />
);

export function AddressInput({ address, setAddress, disabled, errors }) {
  const { address1, address2, city, state, zipCode } = address;

  return (
    <>
      <AddressLine
        label="Address Line 1"
        disabled={disabled}
        value={address1}
        onChange={e => {
          const val = e.target.value;
          setAddress((prev) => ({ ...prev, address1: val }));
        }}
        errors={!disabled && errors.address}
      />
      <AddressLine
        label="Address Line 2"
        disabled={disabled}
        value={address2}
        onChange={e => {
          const val = e.target.value;
          setAddress((prev) => ({ ...prev, address2: val }));
        }}
      />
      <FlexWrapper>
        <GenerationInput
          label="City"
          disabled={disabled}
          value={city}
          onChange={e => {
            const val = e.target.value;
            setAddress((prev) => ({ ...prev, city: val }));
          }}
          errors={!disabled && errors.city}
        />
        <GenerationSelect
          label="State"
          disabled={disabled}
          value={state}
          onChange={val => {
            setAddress((prev) => ({ ...prev, state: val }));
          }}
          options={US_STATES.map(state => ({ value: state[0], label: state[1] }))}
          errors={!disabled && errors.state}
        />
        <GenerationInput
          label="Zip Code"
          disabled={disabled}
          value={zipCode}
          maxLength={5}
          onChange={e => {
            const val = e.target.value;
            setAddress((prev) => ({ ...prev, zipCode: val }));
          }}
          errors={!disabled && errors.zipCode}
        />
      </FlexWrapper>
    </>
  );
}

export function AttorneyInput({ attorney, setAttorney, errors }) {
  const [attornies, setAttornies] = useState([]);

  useEffect(() => {
    let isMounted = true;
    (async function() {
      try {
        const { data } = await Axios.get('/contact/?category=attorney');
        // only update state when component is mounted
        if (isMounted)
          setAttornies(data?.results || []);
      } catch (error) {
        console.error(error);
      }
    })();
    return () => isMounted = false;
  }, []);

  return (
    <>
      <GenerationSelect
        label="Attorney Name"
        value={attorney}
        onChange={val => setAttorney(val)}
        options={attornies.map(att => ({
          value: att.pk,
          label: att.name,
          address: {
            address1: att.address1,
            address2: att.address2,
            city: att.city,
            state: {
              label: att.state,
              value: att.state,
            },
            zipCode: att.zipcode,
          },
        }))}
        errors={errors.attorney}
      />
      {attorney && 
        <AddressInput address={attorney.address} disabled />
      }
    </>
  );
}
