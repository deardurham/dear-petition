import React, { useState, useEffect } from 'react';
import { GenerationPageStyled, PetitionsList, GenerationContentStyled } from './GenerationPage.styled';
import { useParams } from 'react-router-dom';
import GenerationInputs from './GenerationInputs';
import PetitionListItem from './PetitionListItem';

const FAKE_RESPONSE = {
  "id": 100,
  "label": "John Doe",
  "petitions": [
    { "id": 200, "type": "AOC-CR-287", "county": "Durham", "court": "District" },
    { "id": 201, "type": "AOC-CR-288", "county": "Wake", "court": "District" }
  ]
}

function GenerationPage(props) {
  const { batchId } = useParams();
  const [loading, setLoading] = useState();
  const [batch, setBatch] = useState();

  useEffect(() => {
    setLoading(true);
    let timeout = setTimeout(() => {
      setBatch(FAKE_RESPONSE);
      setLoading(false);
    }, 1000)
  }, [batchId])

  return (
    <GenerationPageStyled>
      {loading
        ? <h2>Loading...</h2>
        : (
          <GenerationContentStyled>
            <h2>{batch?.label}</h2>
            <GenerationInputs s />
            <PetitionsList>
              {batch?.petitions?.map(petition => {
                return <PetitionListItem key={petition.id} petition={petition} />
              })}
            </PetitionsList>
          </GenerationContentStyled>
        )
      }
    </GenerationPageStyled>
  );
}

export default GenerationPage;
