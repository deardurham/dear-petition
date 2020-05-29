import React, { useState, useEffect, useContext } from 'react';
import { GenerationInputsStyled, GenerationInputWrapper } from './GenerationInputs.styled';
// Constants
import US_STATES from '../../../constants/US_STATES';

// Ajax
import Axios from '../../../service/axios';

// Children
import Input from '../../elements/Input/Input';
import Select from '../../elements/Input/Select';
import { GenerationContext } from './GenerationPage';

function GenerationInputs() {
  const [attornies, setAttornies] = useState([]);
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
    </GenerationInputsStyled>
  );
}

export default GenerationInputs;
