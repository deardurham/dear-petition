import React, { useState, useEffect, createContext } from 'react';
import {
  GenerationPageStyled,
  PetitionsList,
  GenerationContentStyled
} from './GenerationPage.styled';

// Router
import { useParams } from 'react-router-dom';

// AJAX
import Axios from '../../../service/axios';

// Children
import GenerationInputs from './GenerationInputs';
import PetitionListItem from './PetitionListItem';

export const GenerationContext = createContext(null);

function GenerationPage() {
  const { batchId } = useParams();
  const [loading, setLoading] = useState();
  const [batch, setBatch] = useState();
  const [petition, setPetition] = useState();
  const [ssn, setSSN] = useState('');
  const [licenseNumber, setLicenseNumber] = useState('');
  const [licenseState, setLicenseState] = useState({ label: 'NC', value: 'NC' });
  const [attorney, setAttorney] = useState('');
  const [selectedAgencies, setSelectedAgencies] = useState([]);
  const [showGenerationModal, setShowGenerationModal] = useState(false);
  const [formErrors, setFormErrors] = useState({});

  useEffect(() => {
    setLoading(true);
    Axios.get(`/batch/${batchId}/`)
      .then(({ data }) => {
        setBatch(data);
        setLoading(false);
      })
      .catch(error => {
        console.error(error);
        setLoading(false);
      });
  }, [batchId]);

  const _petitionDataIsValid = () => {
    let isValid = true;
    const errors = {};
    if (!ssn) {
      errors.ssn = ['This field is required'];
      isValid = false;
    }
    if (!licenseNumber) {
      errors.licenseNumber = ['This field is required'];
      isValid = false;
    }
    if (!licenseState) {
      errors.licenseState = ['This field is required'];
      isValid = false;
    }
    if (!attorney) {
      errors.attorney = ['This field is required'];
      isValid = false;
    }

    setFormErrors(errors);

    return isValid;
  };

  const handlePetitionSelect = selectedPetition => {
    setFormErrors({});
    if (_petitionDataIsValid()) {
      setPetition(selectedPetition);
      setShowGenerationModal(true);
    }
  };

  const context = {
    batch,
    petition,
    ssn,
    setSSN,
    licenseNumber,
    setLicenseNumber,
    licenseState,
    setLicenseState,
    attorney,
    setAttorney,
    selectedAgencies,
    setSelectedAgencies,
    showGenerationModal,
    setShowGenerationModal,
    formErrors,
    setFormErrors,
    handlePetitionSelect
  };

  return (
    <GenerationContext.Provider value={context}>
      <GenerationPageStyled>
        {loading ? (
          <h2>Loading...</h2>
        ) : (
          <GenerationContentStyled>
            <h2>{batch?.label}</h2>
            <GenerationInputs />
            <PetitionsList>
              {batch?.petitions?.map(petition => {
                return <PetitionListItem key={petition.pk} petition={petition} />;
              })}
            </PetitionsList>
          </GenerationContentStyled>
        )}
      </GenerationPageStyled>
    </GenerationContext.Provider>
  );
}

export default GenerationPage;
