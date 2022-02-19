import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import Axios from '../../../service/axios';
import { useParams } from 'react-router-dom';

import { DetailRecordPageStyled } from './DetailRecordPage.styled';
import HighlightTable from '../../elements/HighlightTable/HighlightTable';
import AttorneyInput from '../GenerationPage/GenerationInput/AttorneyInput';
import PetitionerInput from '../GenerationPage/GenerationInput/PetitionerInput';
import InputSection from '../../elements/Input/InputSection';
import { Button } from '../../elements/Button';
import PetitionList from '../GenerationPage/PetitionList';

const DEFAULT_STATE_LABEL = { label: 'NC', value: 'NC' };

const REQUIRED_FIELDS = ['name', 'address1', 'city', 'state', 'zipCode'];

const ButtonStyled = styled(Button)`
  font-size: 1.5rem;
  margin: 1rem;
`;

function PageButton({ label, onClick, disabled }) {
  return (
    <ButtonStyled onClick={onClick} disabled={disabled}>
      {label}
    </ButtonStyled>
  );
}

function DetailRecordPage() {
  const { petitionId } = useParams();
  const [loading, setLoading] = useState();
  const [offenseRecords, setOffenseRecords] = useState();
  const [highlightedRows, setHighlightedRows] = useState([]);
  const [generatePetition, setGeneratePetition] = useState();
  const [attorney, setAttorney] = useState('');
  const [petitionsCalculated, setPetitionsCalculated] = useState();
  const [petitions, setPetitions] = useState();
  const [petitionerData, setPetitionerData] = useState({
    name: '',
    address1: '',
    address2: '',
    city: '',
    state: DEFAULT_STATE_LABEL,
    zipCode: '',
  });
  const [formErrors, setFormErrors] = useState({});
  const [county, setCounty] = useState();
  const [jurisdiction, setJurisdiction] = useState();
  const [formType, setFormType] = useState();

  useEffect(() => {
    setLoading(true);
    console.log('Calling the API again');
    Axios.get(`/petitions/${petitionId}/`).then(({ data }) => {
      setOffenseRecords(data.offense_records);
      setCounty(data.county);
      setJurisdiction(data.jurisdiction);
      setFormType(data.formType);
      setLoading(false);
    });
  }, []);

  const highlightRow = (offenseRecordId) => {
    setHighlightedRows([...highlightedRows, offenseRecordId]);
  };

  const unhighlightRow = (offenseRecordId) => {
    setHighlightedRows(highlightedRows.filter((value, index, arr) => value !== offenseRecordId));
  };

  const recalculatePetitions = () => {
    Axios.post(`/petitions/${petitionId}/recalculate_petitions/`, {
      offense_record_ids: highlightedRows,
    }).then(({ data }) => {
      setPetitions(data);
    });
  };

  const validateInput = () => {
    let hasErrors = false;
    if (!attorney) {
      setFormErrors((oldErrors) => ({
        ...oldErrors,
        attorney: ['Please select an attorney from the list'],
      }));
      hasErrors = true;
    }
    REQUIRED_FIELDS.forEach((key) => {
      if (!petitionerData[key]) {
        setFormErrors((oldErrors) => ({ ...oldErrors, [key]: ['This field is required'] }));
        hasErrors = true;
      }
    });
    if (!hasErrors) {
      setGeneratePetition(true);
    }
  };

  const clearError = (key) => {
    if (formErrors[key]) {
      setFormErrors((oldErrors) => ({ ...oldErrors, [key]: [] }));
    }
  };

  return (
    <DetailRecordPageStyled>
      {loading ? (
        <h3>Loading...</h3>
      ) : (
        <div>
          <InputSection label="Attorney Information">
            <AttorneyInput
              attorney={attorney}
              setAttorney={setAttorney}
              errors={formErrors}
              onClearError={clearError}
            />
          </InputSection>
          <InputSection label="Petitioner Information">
            <PetitionerInput
              petitionerData={petitionerData}
              setPetitionerData={setPetitionerData}
              errors={formErrors}
              onClearError={clearError}
            />
          </InputSection>
          <h2>Offense Record List</h2>
          <h3>
            County: {county} Jurisdiction: {jurisdiction} Form Type: {formType}
          </h3>
          <HighlightTable
            offenseRecords={offenseRecords}
            highlightRow={highlightRow}
            unhighlightRow={unhighlightRow}
          />
          <PageButton label="Update Petitions" onClick={recalculatePetitions} />
          {petitions ? (
            <div>
              <h2>Petition List</h2>
              <PetitionList
                petitions={petitions}
                attorney={attorney}
                petitionerData={petitionerData}
                validateInput={validateInput}
              />
            </div>
          ) : null}
        </div>
      )}
    </DetailRecordPageStyled>
  );
}

export default DetailRecordPage;
