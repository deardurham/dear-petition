import React, { useState, useEffect } from 'react';
import { AddressLine, FlexWrapper, GenerationInput, GenerationSelect } from './GenerationInputs.styled';
// Constants
import US_STATES from '../../../constants/US_STATES';

// Ajax
import Axios from '../../../service/axios';

export function AddressInput({ address, setAddress, disabled, errors }) {
  const [address1, setAddress1] = useState(address.address1);
  const [address2, setAddress2] = useState(address.address2);
  const [city, setCity] = useState(address.city);
  const [state, setState] = useState(address.state);
  const [zipCode, setZipCode] = useState(address.zipCode);

  return (
    <>
      <AddressLine
        label="Address Line 1"
        disabled={disabled}
        value={address1}
        onChange={e => {
          const val = e.target.value;
          setAddress1(val);
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
          setAddress2(val);
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
            setCity(val);
            setAddress((prev) => ({ ...prev, city: val }));
          }}
          errors={!disabled && errors.city}
        />
        <GenerationSelect
          label="State"
          disabled={disabled}
          value={state}
          onChange={val => {
            setState(val);
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
            setZipCode(val);
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
