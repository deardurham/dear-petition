import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import {
  GenerationPageStyled,
  GenerationContentStyled
} from './GenerationPage.styled';

// Router
import { useParams } from 'react-router-dom';

// AJAX
import Axios from '../../../service/axios';

// Children
import AttorneyInput from './GenerationInput/AttorneyInput';
import PetitionerInput from './GenerationInput/PetitionerInput';
import PetitionList from './PetitionList';

const DEFAULT_STATE_LABEL = { label: 'NC', value: 'NC' };

const GenerationSection = styled.div`
  margin-bottom: 2rem;

  & h2 {
    margin-bottom: 2rem;
    user-select: none;
  }
`;

const InputSection = styled(GenerationSection)`
  width: 80%;
  min-width: 400px;
`;

function GenerationPage() {
  const { batchId } = useParams();
  const [loading, setLoading] = useState();
  const [batch, setBatch] = useState();
  const [petitionerData, setPetitionerData] = useState({
    name: '',
    ssn: '',
    licenseNumber: '',
    licenseState: DEFAULT_STATE_LABEL,
    address1: '',
    address2: '',
    city: '',
    state: DEFAULT_STATE_LABEL,
    zipCode: '',
  });
  const [attorney, setAttorney] = useState('');
  const [formErrors, setFormErrors] = useState({});

  useEffect(() => {
    setLoading(true);
    Axios.get(`/batch/${batchId}/`)
      .then(({ data }) => {
        setBatch(data);
        setPetitionerData(prev => ({ ...prev, name: data?.label }));
        setLoading(false);
      })
      .catch(error => {
        console.error(error);
        setLoading(false);
      });
  }, [batchId]);

  const clearError = (key) => {
    formErrors[key] && setFormErrors((oldErrors) => ({ ...oldErrors, [key]: [] }));
  };

  return (
    <GenerationPageStyled>
      {loading ? (
        <h3>Loading...</h3>
      ) : (
        <GenerationContentStyled>
          <InputSection>
            <h2>Attorney Information</h2>
            <AttorneyInput
              attorney={attorney}
              setAttorney={setAttorney}
              errors={formErrors}
              onClearError={clearError}
            />
          </InputSection>
          <InputSection>
            <h2>Petitioner Information</h2>
            <PetitionerInput
              petitionerData={petitionerData}
              setPetitionerData={setPetitionerData}
              errors={formErrors}
              onClearError={clearError}
            />
          </InputSection>
          <GenerationSection>
            <h2>Petition List</h2>
            <PetitionList
              petitions={batch?.petitions || []}
              attorney={attorney}
              petitionerData = {petitionerData}
              onError={(errorObj) => setFormErrors((oldErrors) => ({ ...oldErrors, ...errorObj }))}
            />
          </GenerationSection>
        </GenerationContentStyled>
      )}
    </GenerationPageStyled>
  );
}

export default GenerationPage;
