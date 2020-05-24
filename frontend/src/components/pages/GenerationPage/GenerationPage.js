import React, { useState, useEffect, createContext } from 'react';
import {
  GenerationPageStyled,
  PetitionsList,
  GenerationContentStyled
} from './GenerationPage.styled';
import { useParams } from 'react-router-dom';
import GenerationInputs from './GenerationInputs';
import PetitionListItem from './PetitionListItem';

const FAKE_RESPONSE = {
  id: 100,
  label: 'John Doe',
  petitions: [
    { id: 200, type: 'AOC-CR-287', county: 'Durham', court: 'District' },
    { id: 201, type: 'AOC-CR-288', county: 'Wake', court: 'District' }
  ]
};

export const GenerationContext = createContext(null);

function GenerationPage(props) {
  const { batchId } = useParams();
  const [loading, setLoading] = useState();
  const [batch, setBatch] = useState();
  const [petition, setPetition] = useState();
  const [ssn, setSSN] = useState('');
  const [license, setLicense] = useState('');
  const [attorney, setAttorney] = useState('');

  useEffect(() => {
    setLoading(true);
    setTimeout(() => {
      setBatch(FAKE_RESPONSE);
      setLoading(false);
    }, 1000);
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
  }

  return (
    <GenerationContext.Provider value={context}>
      <GenerationPageStyled>
        {loading ? (
          <h2>Loading...</h2>
        ) : (
            <GenerationContentStyled>
              <h2>{batch?.label}</h2>
              <GenerationInputs s />
              <PetitionsList>
                {batch?.petitions?.map(petition => {
                  return <PetitionListItem key={petition.id} petition={petition} />;
                })}
              </PetitionsList>
            </GenerationContentStyled>
          )}
      </GenerationPageStyled>
    </GenerationContext.Provider >
  );
}

export default GenerationPage;
