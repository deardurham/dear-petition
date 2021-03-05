import React, { useState } from 'react';
import styled from 'styled-components';
import { greyScale } from '../../../styles/colors';
import {
  GenerateButtonCell,
  PetitionListItemStyled,
  PetitionCellStyled,
  PetitionListHeader
} from './PetitionList.styled';
import { Button } from '../../elements/Button/Button.styled';
import GeneratePetitionModal from './GeneratePetitionModal/GeneratePetitionModal';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPlay } from '@fortawesome/free-solid-svg-icons';

export function PetitionList({ children, className }) {
  return (
    <ul className={className}>
      <PetitionListHeader>
        <PetitionCellStyled>County</PetitionCellStyled>
        <PetitionCellStyled>Jurisdiction</PetitionCellStyled>
        <PetitionCellStyled>Form Type</PetitionCellStyled>
        <GenerateButtonCell />
      </PetitionListHeader>
      {children}
    </ul>
  );
}

const GenerateButton = styled(Button)`
  font-size: 1.4rem;
`;

const FormType = styled.div`
  margin-right: 4rem;
`;

const Attachments = styled.div`
  margin-left: 2rem;
  margin-right: 2rem;
  display: flex;
  flex-flow: column;

  & > div {
    padding: 1rem;
  }
`;

const SelectableRow = styled.div`
  font-size: 1.6rem;
  padding: 2rem;
  display: flex;
  &:hover {
    background: ${greyScale(8)};
  }
`;

export function PetitionListItem({ attorney, petition, petitionerData, setPetitionerData }) {
  const [isVisible, setVisible] = useState(false);
  const [wasGenerated, setGenerated] = useState(false);

  return (
    <>
      <PetitionListItemStyled>
        <SelectableRow onClick={() => { setVisible(true); setGenerated(true) }}>
          <PetitionCellStyled>{petition.county} County</PetitionCellStyled>
          <PetitionCellStyled>{petition.jurisdiction}</PetitionCellStyled>
          <PetitionCellStyled>{petition.form_type}</PetitionCellStyled>
          <GenerateButtonCell>
            <GenerateButton>{wasGenerated ? "Regenerate" : 'Generate'}</GenerateButton>
          </GenerateButtonCell>
        </SelectableRow>
        {petition.attachments.length > 0 && (
          <Attachments>
            <h4>Attachments:</h4>
            {petition.attachments.map(attachment => (
              <SelectableRow key={attachment.pk} onClick={() => setVisible(true)}>
                <FormType>{attachment.form_type}</FormType>
                <GenerateButton>Generate</GenerateButton>
              </SelectableRow>
            ))}
          </Attachments>
        )}
      </PetitionListItemStyled>
      {isVisible && (
        <GeneratePetitionModal
          petition={petition}
          petitionerData={petitionerData}
          attorney={attorney}
          setPetitionerData={setPetitionerData}
          onClose={() => setVisible(false)}
        />
      )}
    </>
  );
}
