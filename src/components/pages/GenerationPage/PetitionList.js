import React, { useState } from 'react';
import {
  GenerateButtonCell,
  PetitionListItemStyled,
  PetitionCellStyled,
  PetitionListHeader
} from './PetitionList.styled';
import GeneratePetitionModal from './GeneratePetitionModal/GeneratePetitionModal';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPlay } from '@fortawesome/free-solid-svg-icons';
import { AgencyInput } from './GenerationInputs';

export function PetitionList({ children, className }) {
  return (
    <ul className={className}>
      <PetitionListHeader>
        <PetitionCellStyled>Form Type</PetitionCellStyled>
        <PetitionCellStyled>County</PetitionCellStyled>
        <PetitionCellStyled>Jurisdiction</PetitionCellStyled>
      </PetitionListHeader>
      {children}
    </ul>
  );
}

const GenerateButton = () => <FontAwesomeIcon icon={faPlay} />;

export function PetitionListItem({ petition, petitionerData, setPetitionerData }) {
  const [isVisible, setVisible] = useState(false);

  return (
    <>
      <PetitionListItemStyled onClick={() => setVisible(true)}>
        <PetitionCellStyled>{petition.form_type}</PetitionCellStyled>
        <PetitionCellStyled>{petition.county} County</PetitionCellStyled>
        <PetitionCellStyled>{petition.jurisdiction}</PetitionCellStyled>
        <GenerateButtonCell>
          <GenerateButton />
        </GenerateButtonCell>
      </PetitionListItemStyled>
      {isVisible && (
        <GeneratePetitionModal
          petition={petition}
          petitionerData={petitionerData}
          setPetitionerData={setPetitionerData}
          onClose={() => setVisible(false)}
        />
      )}
    </>
  );
}
