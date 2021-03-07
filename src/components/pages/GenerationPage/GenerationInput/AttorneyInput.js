import React, { useState, useEffect } from 'react';
import Axios from '../../../../service/axios';
import Select from '../../../elements/Input/Select';
import AddressInput from './AddressInput';

export default function AttorneyInput({ attorney, setAttorney, errors, onClearError }) {
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
      <Select
        label="Attorney Name"
        value={attorney}
        onChange={val => {
          setAttorney(val);
          onClearError('attorney');
        }}
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
