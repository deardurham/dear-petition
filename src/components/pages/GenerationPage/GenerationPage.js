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
import { colorBlue } from '../../../styles/colors';

const DEFAULT_STATE_LABEL = { label: 'NC', value: 'NC' };

const GenerationSection = styled.div`
  margin: 0rem 0rem 2rem 0rem;
`;

const Button = styled.button`
  border: none;
  color: ${colorBlue};
  cursor: pointer;
`;

function CollapsibleSection({ label, children }) {
  const [collapsed, setCollapsed] = useState(false);
  return (
    <GenerationSection>
      <FlexWrapper>
        <h3>{label}</h3>
        <Button onClick={() => setCollapsed(!collapsed)}>{collapsed ? 'Edit' : 'Save'}</Button>
      </FlexWrapper>
      {!collapsed && children}
    </GenerationSection>
  );
}

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
          <CollapsibleSection label='Attorney Information'>
            <AttorneyInput attorney={attorney} setAttorney={setAttorney} errors={formErrors} />
          </CollapsibleSection>
          <CollapsibleSection label='Petitioner Information'>
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
          </CollapsibleSection>
          <GenerationSection>
            <h3>Petition List</h3>
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
