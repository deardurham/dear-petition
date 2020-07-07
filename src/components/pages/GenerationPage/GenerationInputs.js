import React, { useState, useEffect, useContext } from 'react';
import { FlexWrapper, GenerationInputsStyled, GenerationInputWrapper } from './GenerationInputs.styled';
// Constants
import US_STATES from '../../../constants/US_STATES';

// Ajax
import Axios from '../../../service/axios';

// Children
import Input from '../../elements/Input/Input';
import Select from '../../elements/Input/Select';
import { GenerationContext } from './GenerationPage';

function AddressInput({ setAddress, errors }) {
  const [address1, setAddress1] = useState('');
  const [address2, setAddress2] = useState('');
  const [city, setCity] = useState('');
  const [state, setState] = useState({ label: 'NC', value: 'NC' });
  const [zipCode, setZipCode] = useState('');
  return (
    <FlexWrapper>
      <GenerationInputWrapper>
        <Input
          label="Address Line 1"
          value={address1}
          onChange={e => {
            const val = e.target.value;
            setAddress1(val);
            setAddress((prev) => ({ ...prev, address1: val }));
          }}
          errors={errors.address}
        />
      </GenerationInputWrapper>

      <GenerationInputWrapper>
        <Input
          label="Address Line 2"
          value={address2}
          onChange={e => {
            const val = e.target.value;
            setAddress2(val);
            setAddress((prev) => ({ ...prev, address2: val }));
          }}
        />
      </GenerationInputWrapper>

      <GenerationInputWrapper>
        <Input
          label="City"
          value={city}
          onChange={e => {
            const val = e.target.value;
            setCity(val);
            setAddress((prev) => ({ ...prev, city: val }));
          }}
          errors={errors.city}
        />
      </GenerationInputWrapper>

      <GenerationInputWrapper>
        <Select
          label="State"
          value={state}
          onChange={val => {
            setState(val);
            setAddress((prev) => ({ ...prev, state: val }));
          }}
          options={US_STATES.map(state => ({ value: state[0], label: state[0] }))}
          errors={errors.state}
        />
      </GenerationInputWrapper>

      <GenerationInputWrapper>
        <Input
          label="Zip Code"
          value={zipCode}
          maxLength={5}
          onChange={e => {
            const val = e.target.value;
            setZipCode(val);
            setAddress((prev) => ({ ...prev, zipCode: val }));
          }}
          errors={errors.zipCode}
        />
      </GenerationInputWrapper>
    </FlexWrapper>
  );
}

function GenerationInputs() {
  const [attornies, setAttornies] = useState([]);
  const {
    attorney,
    ssn,
    licenseNumber,
    licenseState,
    address,
    setAttorney,
    setSSN,
    setLicenseNumber,
    setLicenseState,
    setAddress,
    formErrors
  } = useContext(GenerationContext);

  useEffect(() => {
    (async function() {
      try {
        const { data } = await Axios.get('/contact/?category=attorney');
        setAttornies(data?.results || []);
      } catch (error) {
        console.error(error);
      }
    })();
  }, []);

  return (
    <GenerationInputsStyled>
      <FlexWrapper>
        <GenerationInputWrapper>
          <Select
            label="Attorney"
            value={attorney}
            onChange={val => setAttorney(val)}
            options={attornies.map(att => ({ value: att.pk, label: att.name }))}
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
      </FlexWrapper>

      <AddressInput setAddress={setAddress} errors={formErrors} />
    </GenerationInputsStyled>
  );
}

export default GenerationInputs;
