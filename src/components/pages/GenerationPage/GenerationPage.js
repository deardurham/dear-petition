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
import { AddressInput, AttorneyInput } from './GenerationInputs';
import { GenerationInput, GenerationSelect, FlexWrapper, SSN } from './GenerationInputs.styled';
import { PetitionListStyled } from './PetitionList.styled'
import { PetitionListItem } from './PetitionList';
import US_STATES from '../../../constants/US_STATES';

const DEFAULT_STATE_LABEL = { label: 'NC', value: 'NC' };

const SectionDiv = styled.div`
  margin-bottom: 1rem;
  min-width: 400px;
  max-width: 1000px;
  width: 80%;
`;

const SectionHeader = styled.h3`
  margin-bottom: 2rem;
  user-select: none;
`;

const GenerationSection = ({ label, children }) => (
  <SectionDiv>
    <SectionHeader>{label}</SectionHeader>
    {children}
  </SectionDiv>
);

function GenerationPage() {
  const { batchId } = useParams();
  const [loading, setLoading] = useState();
  const [batch, setBatch] = useState();
  const [petitionerName, setPetitionerName] = useState('');
  const [ssn, setSSN] = useState('');
  const [address, setAddress] = useState({
    address1: '',
    address2: '',
    city: '',
    state: DEFAULT_STATE_LABEL,
    zipCode: '',
  });
  const [licenseNumber, setLicenseNumber] = useState('');
  const [licenseState, setLicenseState] = useState(DEFAULT_STATE_LABEL);
  const [attorney, setAttorney] = useState('');
  const [formErrors, setFormErrors] = useState({});

  useEffect(() => {
    setLoading(true);
    Axios.get(`/batch/${batchId}/`)
      .then(({ data }) => {
        setBatch(data);
        setPetitionerName(data?.label);
        setLoading(false);
      })
      .catch(error => {
        console.error(error);
        setLoading(false);
      });
  }, [batchId]);

  return (
    <GenerationPageStyled>
      {loading ? (
        <h3>Loading...</h3>
      ) : (
        <GenerationContentStyled>
          <GenerationSection label='Attorney Information'>
            <AttorneyInput attorney={attorney} setAttorney={setAttorney} errors={formErrors} />
          </GenerationSection>
          <GenerationSection label='Petitioner Information'>
            <FlexWrapper>
              <GenerationInput
                label='Petitioner Name'
                value={petitionerName}
                onChange={e => setPetitionerName(e.target.value)}
                errors={formErrors.petitionerName}
              />
              <SSN
                label='SSN'
                value={ssn}
                maxLength={11}
                onChange={e => setSSN(e.target.value.replace(/[^0-9-]/g, ''))}
                errors={formErrors.ssn}
              />
            </FlexWrapper>
            <FlexWrapper>
              <GenerationInput
                label="License #"
                value={licenseNumber}
                onChange={e => setLicenseNumber(e.target.value)}
                errors={formErrors.licenseNumber}
              />
              <GenerationSelect
                label="License state"
                value={licenseState}
                onChange={val => setLicenseState(val)}
                options={US_STATES.map(state => ({ value: state[0], label: state[0] }))}
                errors={formErrors.licenseState}
              />
            </FlexWrapper>
            <AddressInput address={address} setAddress={setAddress} errors={formErrors} />
          </GenerationSection>
          <GenerationSection label='Petition List'>
            <PetitionListStyled>
              {batch?.petitions?.map(petition =>
                <PetitionListItem
                  key={petition.pk}
                  petition={petition}
                  attorney={attorney}
                  petitionerData = {{
                    petitionerName,
                    ssn,
                    address,
                    licenseNumber,
                    licenseState,
                  }}
                  onError={(errors) => setFormErrors(errors)}
                />
              )}
            </PetitionListStyled>
          </GenerationSection>
        </GenerationContentStyled>
      )}
    </GenerationPageStyled>
  );
}

export default GenerationPage;
