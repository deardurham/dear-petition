import React, { useState } from 'react';
import styled from 'styled-components';
import { Button } from '../../elements/Button/Button.styled';
import GeneratePetitionModal from './GeneratePetitionModal/GeneratePetitionModal';
import { TABLET_LANDSCAPE_SIZE } from '../../../styles/media';
import { Table, TableBody, TableCell, TableHeader, TableRow } from '../../elements/Table';
import useWindowSize from '../../../hooks/useWindowSize';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faDownload } from '@fortawesome/free-solid-svg-icons';

const GenerateButtonStyled = styled(Button)`
  font-size: 1.5rem;
`;

const PetitionTable = styled(Table)`
  font-size: 1.7rem;
  font-family: Arial, Helvetica, sans-serif;
`;

const Attachments = styled.ul`
  & > li:not(:last-child) {
    margin-bottom: 1rem;
  }
`;

const Label = styled.span`
  font-size: 1.75rem;
`;

function GenerateButton({ label, windowWidth, onClick, collapsedIcon }) {
  const isCollapsed = windowWidth <= TABLET_LANDSCAPE_SIZE;
  return (
    <GenerateButtonStyled onClick={onClick}>
      {isCollapsed && collapsedIcon ? <FontAwesomeIcon icon={collapsedIcon} /> : label}
    </GenerateButtonStyled>
  );
}

function PetitionRow({ attorney, petition, petitionerData, validateInput }) {
  const [agencies, setAgencies] = useState([]);
  const [attachmentNumber, setAttachmentNumber] = useState();
  const [selectedPetition, setSelectedPetition] = useState();
  const windowSize = useWindowSize();

  const handleSelect = (newPetition, num) => {
    if (validateInput()) {
      setSelectedPetition(newPetition);
      if (num) {
        setAttachmentNumber(num);
      }
    }
  };

  return (
    <>
      <TableRow key={petition.pk}>
        <TableCell>{petition.county}</TableCell>
        <TableCell>{petition.jurisdiction}</TableCell>
        <TableCell>
          <GenerateButton
            collapsedIcon={faDownload}
            windowWidth={windowSize.width}
            label={petition.form_type}
            onClick={() => handleSelect(petition)}
          />
        </TableCell>
        <TableCell>
          <Attachments>
            {petition.attachments.map((attachment, i) => (
              <li key={attachment.pk}>
                <Label>{`${i + 1}) `}</Label>
                <GenerateButton
                  collapsedIcon={faDownload}
                  windowWidth={windowSize.width}
                  label={attachment.form_type}
                  onClick={() => handleSelect(attachment, i + 1)}
                />
              </li>
            ))}
          </Attachments>
        </TableCell>
      </TableRow>
      {selectedPetition && (
        <GeneratePetitionModal
          petition={selectedPetition}
          attachmentNumber={attachmentNumber}
          petitionerData={petitionerData}
          attorney={attorney}
          agencies={agencies}
          setAgencies={setAgencies}
          onClose={() => {
            setSelectedPetition();
            setAttachmentNumber();
          }}
        />
      )}
    </>
  );
}

export default function PetitionList({ attorney, petitions, petitionerData, validateInput }) {
  return (
    <PetitionTable numColumns={4}>
      <TableHeader>
        <TableCell header>County</TableCell>
        <TableCell header>Jurisdiction</TableCell>
        <TableCell header>Primary Form</TableCell>
        <TableCell header>Attachments</TableCell>
      </TableHeader>
      <TableBody>
        {petitions.map(petition => (
          <PetitionRow
            key={petition.pk}
            petition={petition}
            petitionerData={petitionerData}
            attorney={attorney}
            validateInput={validateInput}
          />
        ))}
      </TableBody>
    </PetitionTable>
  );
}
