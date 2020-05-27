import React, { useState, useEffect, createContext } from 'react';
import {
  GenerationPageStyled,
  PetitionsList,
  GenerationContentStyled
} from './GenerationPage.styled';
import { useParams } from 'react-router-dom';
import GenerationInputs from './GenerationInputs';
import PetitionListItem from './PetitionListItem';
import Axios from '../../../service/axios';

export const GenerationContext = createContext(null);

function GenerationPage() {
  const { batchId } = useParams();
  const [loading, setLoading] = useState();
  const [batch, setBatch] = useState();
  const [petition, setPetition] = useState();
  const [ssn, setSSN] = useState('');
  const [license, setLicense] = useState('');
  const [attorney, setAttorney] = useState('');
  const [selectedAgencies, setSelectedAgencies] = useState([]);

  useEffect(() => {
    setLoading(true);
    Axios.get(`/batch/${batchId}/`)
      .then(({ data }) => {
        setBatch(data);
        console.log('setting batch to: ', data);
        setLoading(false);
      })
      .catch(error => {
        console.error(error);
        setLoading(false);
      });
  }, [batchId]);

  const context = {
    batch,
    setBatch,
    petition,
    setPetition,
    ssn,
    setSSN,
    license,
    setLicense,
    attorney,
    setAttorney,
    selectedAgencies,
    setSelectedAgencies,
  }

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
    </GenerationContext.Provider >
  );
}

export default GenerationPage;
