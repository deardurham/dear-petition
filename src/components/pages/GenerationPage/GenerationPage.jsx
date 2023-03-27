import React, { useState } from 'react';
import styled from 'styled-components';
import { GenerationPageStyled, GenerationContentStyled } from './GenerationPage.styled';
import { colorGrey } from '../../../styles/colors';
import { smallerThanTabletLandscape } from '../../../styles/media';
import { saveAs } from 'file-saver';

// Router
import { useParams } from 'react-router-dom';

import { useGetBatchQuery, useUpdateBatchMutation } from '../../../service/api';

// Children
import AttorneyInput from './GenerationInput/AttorneyInput';
import PetitionerInput from './GenerationInput/PetitionerInput';
import PetitionList from './PetitionList';
import Button from '../../elements/Button';
import Axios from '../../../service/axios';

const GenerationSection = styled.div`
  padding: 2rem 0;
  margin-bottom: 2rem;

  & > h2 {
    user-select: none;
    margin-bottom: 2rem;
  }

  & > p {
    font-size: 1.6rem;
    margin-bottom: 2rem;
  }

  & > div > h3 {
    user-select: none;
    margin-bottom: 1rem;
  }
`;

const InputSectionStyled = styled(GenerationSection)`
  display: flex;
  border-bottom: 1px solid ${colorGrey};

  & > div:first-child {
    flex: 1 0 33%;
  }

  & > div:last-child {
    flex: 1 0 66%;
  }

  @media (${smallerThanTabletLandscape}) {
    flex-flow: column;
  }
`;

const InputSection = ({ children, label }) => (
  <InputSectionStyled>
    <div>
      <h3>{label}</h3>
    </div>
    <div className="mt-2 flex flex-col gap-4">{children}</div>
  </InputSectionStyled>
);

const _openDoc = (doc, filename) => {
  const docBlob = new Blob([doc], {
    type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
  });
  saveAs(docBlob, filename);
};

function GenerationPage() {
  const { batchId } = useParams();
  const [formErrors, setFormErrors] = useState({});
  const { data, isLoading } = useGetBatchQuery({ id: batchId });
  const [triggerUpdate] = useUpdateBatchMutation();

  if (isLoading) {
    return (
      <GenerationPageStyled>
        <h3>Loading...</h3>
      </GenerationPageStyled>
    );
  }

  const { attorney, client } = data;

  const validateInput = () => {
    let hasErrors = false;
    if (!attorney) {
      setFormErrors((oldErrors) => ({
        ...oldErrors,
        attorney: ['Please select an attorney'],
      }));
      hasErrors = true;
    }
    if (!client) {
      setFormErrors((oldErrors) => ({
        ...oldErrors,
        client: ['Please select or add a client'],
      }));
      hasErrors = true;
    }
    return !hasErrors;
  };

  const clearError = (key) => {
    if (formErrors[key]) {
      setFormErrors((oldErrors) => ({ ...oldErrors, [key]: [] }));
    }
  };

  const generateAdviceLetter = async () => {
    if (!validateInput()) {
      return;
    }

    Axios.post(
      `/batch/${batchId}/generate_advice_letter/`,
      {},
      {
        responseType: 'arraybuffer',
      }
    ).then((adviceLetter) => {
      _openDoc(adviceLetter.data, 'Advice Letter.docx');
    });
  };

  const generateExpungableSummary = async () => {
    if (!validateInput()) {
      return;
    }

    Axios.post(
      `/batch/${batchId}/generate_expungable_summary/`,
      {},
      {
        responseType: 'arraybuffer',
      }
    ).then((expungableSummary) => {
      _openDoc(expungableSummary.data, 'Expungable Record Summary.docx');
    });
  };

  return (
    <GenerationPageStyled>
      <GenerationContentStyled>
        <InputSection label="Attorney Information">
          <AttorneyInput
            attorney={attorney}
            onSelectAttorney={async (selectedAttorney) => {
              try {
                await triggerUpdate({
                  id: batchId,
                  data: { attorney_id: selectedAttorney.pk },
                }).unwrap();
              } catch (e) {
                setFormErrors((oldErrors) => ({
                  ...oldErrors,
                  attorney: ['Error: Unable to select attorney'],
                }));
              }
            }}
            errors={formErrors}
            onClearError={clearError}
          />
        </InputSection>
        <InputSection label="Petitioner Information">
          <PetitionerInput petitioner={client} errors={formErrors} onClearError={clearError} />
        </InputSection>
        <InputSection label="Documents">
          <div className="flex gap-4">
            <Button onClick={() => generateExpungableSummary()}>
              Create Expungable Record Summary
            </Button>
            <Button onClick={() => generateAdviceLetter()}>Create Advice Letter</Button>
          </div>
        </InputSection>
        <GenerationSection>
          <h2>Petition List</h2>
          <p>
            Click on the buttons below to generate petition forms and their attachments. Click on
            the &rsquo;View&rsquo; button to reveal a list of offense records.
          </p>
          {data && (
            <PetitionList
              petitions={data?.petitions || []}
              validateInput={validateInput}
              setFormErrors={setFormErrors}
            />
          )}
        </GenerationSection>
      </GenerationContentStyled>
    </GenerationPageStyled>
  );
}

export default GenerationPage;
