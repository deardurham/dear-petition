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

const DEFAULT_STATE_LABEL = { label: 'NC', value: 'NC' };

function GenerationPage() {
  const { batchId } = useParams();
  const [loading, setLoading] = useState();
  const [batch, setBatch] = useState();
  const [selectedPetition, setSelectedPetition] = useState();
  const [petitionerName, setPetitionerName] = useState('');
  const [address, setAddress] = useState({ state: DEFAULT_STATE_LABEL });
  const [ssn, setSSN] = useState('');
  const [licenseNumber, setLicenseNumber] = useState('');
  const [licenseState, setLicenseState] = useState(DEFAULT_STATE_LABEL);
  const [attorney, setAttorney] = useState('');
  const [selectedAgencies, setSelectedAgencies] = useState([]);
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

  const _petitionDataIsValid = () => {
    let isValid = true;
    const errors = {};
    if (!petitionerName) {
      errors.petitionerName = ['This field is required'];
      isValid = false;
    }
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
    if (!address?.address1) {
      errors.address = ['This field is required'];
      isValid = false;
    }
    if (!address?.city) {
      errors.city = ['This field is required'];
      isValid = false;
    }
    if (!address?.state) {
      errors.state = ['This field is required'];
      isValid = false;
    }
    if (!address?.zipCode) {
      errors.zipCode = ['This field is required'];
      isValid = false;
    }

    setFormErrors(errors);

    return isValid;
  };

  const validatePetitionSelect = (petition) => {
    setFormErrors({});
    if (_petitionDataIsValid()) {
      setSelectedPetition(petition);
      return true;
    } else {
      return false;
    }
  };

  const context = {
    batch,
    petition: selectedPetition,
    address,
    setAddress,
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
    petitionerName,
    setPetitionerName,
    formErrors,
    setFormErrors,
  };

  return (
    <GenerationContext.Provider value={context}>
      <GenerationPageStyled>
        {loading ? (
          <h2>Loading...</h2>
        ) : (
          <GenerationContentStyled>
            <GenerationInputs />
            <PetitionsList>
              {batch?.petitions?.map(petition =>
                <PetitionListItem
                  key={petition.pk}
                  petition={petition}
                  validatePetitionSelect={validatePetitionSelect} />
              )}
            </PetitionsList>
          </GenerationContentStyled>
        )}
      </GenerationPageStyled>
    </GenerationContext.Provider>
  );
}

export default GenerationPage;
