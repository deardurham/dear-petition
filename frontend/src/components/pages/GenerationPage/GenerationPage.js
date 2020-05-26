import React, { useState, useEffect } from 'react';
import {
  GenerationPageStyled,
  PetitionsList,
  GenerationContentStyled
} from './GenerationPage.styled';
import { useParams } from 'react-router-dom';
import GenerationInputs from './GenerationInputs';
import PetitionListItem from './PetitionListItem';
import Axios from '../../../service/axios';

function GenerationPage(props) {
  const { batchId } = useParams();
  const [loading, setLoading] = useState();
  const [batch, setBatch] = useState();

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

  return (
    <GenerationPageStyled>
      {loading ? (
        <h2>Loading...</h2>
      ) : (
        <GenerationContentStyled>
          <h2>{batch?.label}</h2>
          <GenerationInputs />
          <PetitionsList>
            {batch?.petitions?.map(petition => {
              return <PetitionListItem key={petition.id} petition={petition} />;
            })}
          </PetitionsList>
        </GenerationContentStyled>
      )}
    </GenerationPageStyled>
  );
}

export default GenerationPage;
