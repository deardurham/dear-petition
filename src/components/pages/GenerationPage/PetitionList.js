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
import { TABLET_LANDSCAPE_SIZE } from '../../../styles/media';
import useWindowSize from '../../../hooks/useWindowSize';

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

const GenerateButtonStyled = styled(Button)`
  font-size: 1.4rem;
`;

function GenerateButton({ label, windowWidth }) {
  const isDesktop = windowWidth >= TABLET_LANDSCAPE_SIZE;
  return (
    <GenerateButtonStyled>
      {isDesktop ? label : <FontAwesomeIcon icon={faPlay} />}
    </GenerateButtonStyled>
  );
}

const AttachmentCell = styled.div`
  display: flex;
  flex: 0 0 29.2%;
`;

const FormType = styled.div`
  margin-left: 1rem;
`;

const Attachments = styled.div`
  margin-left: 2rem;
  margin-right: 2rem;
  display: flex;
  flex-flow: column;

  & > div {
    padding: 1rem;
  }

  & > h4 {
    margin-bottom: 1rem;
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

function AttachListItem({ i, attachment, setVisible }) {
  const [wasAttachGenerated, setAttachGenerated] = useState(false);
  const windowSize = useWindowSize();
  return (
    <SelectableRow key={attachment.pk} onClick={() => { setVisible(true); setAttachGenerated(true) }}>
      <AttachmentCell>
        <span>{`${i+1})`}</span>
        <FormType>{attachment.form_type}</FormType>
      </AttachmentCell>
      <GenerateButton label={wasAttachGenerated ? 'Re-generate' : 'Generate'} windowWidth={windowSize.width} />
    </SelectableRow>
  );
}

export function PetitionListItem({ attorney, petition, petitionerData, setPetitionerData }) {
  const [isVisible, setVisible] = useState(false);
  const [wasGenerated, setGenerated] = useState(false);
  const windowSize = useWindowSize();

  return (
    <>
      <PetitionListItemStyled>
        <SelectableRow
          onClick={() => {
            setVisible(true);
            setGenerated(true);
          }}
        >
          <PetitionCellStyled>{petition.county} County</PetitionCellStyled>
          <PetitionCellStyled>{petition.jurisdiction}</PetitionCellStyled>
          <PetitionCellStyled>{petition.form_type}</PetitionCellStyled>
          <GenerateButtonCell>
            <GenerateButton label={wasGenerated ? 'Re-generate' : 'Generate'} windowWidth={windowSize.width} />
          </GenerateButtonCell>
        </SelectableRow>
        {petition.attachments.length > 0 && (
          <Attachments>
            <h4>Attachments:</h4>
            {petition.attachments.map((attachment, i) => (
              <AttachListItem
                key={attachment.pk}
                attachment={attachment}
                i={i}
                setVisible={setVisible}
              />
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
