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

function GenerateButton({ label, windowWidth, onClick, collapsedIcon }) {
  const isCollapsed = windowWidth < TABLET_LANDSCAPE_SIZE;
  return (
    <GenerateButtonStyled onClick={onClick}>
      {isCollapsed && collapsedIcon ? <FontAwesomeIcon icon={collapsedIcon} /> : label}
    </GenerateButtonStyled>
  );
}

const Attachments = styled.ul`
  & > li:not(:last-child) {
    margin-bottom: 1rem;
  }
`;

const REQUIRED_FIELDS = [
  'name',
  'ssn',
  'licenseNumber',
  'licenseState',
  'address1',
  'city',
  'state',
  'zipCode'
];

export default function PetitionList({ petitions, attorney, petitionerData, onError }) {
  const [selectedPetition, setSelectedPetition] = useState();
  const windowSize = useWindowSize();

  const handleSelect = petition => {
    let hasErrors = false;
    if (!attorney) {
      onError({ attorney: ['Please select an attorney from the list'] });
      hasErrors = true;
    }
    REQUIRED_FIELDS.forEach(key => {
      if (!petitionerData[key]) {
        onError({ [key]: ['This field is required'] });
        hasErrors = true;
      }
    });
    if (!hasErrors) {
      setSelectedPetition(petition);
    }
  };

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
                    <span>{`${i + 1}) `}</span>
                    <GenerateButton
                      collapsedIcon={faDownload}
                      windowWidth={windowSize.width}
                      label={attachment.form_type}
                      onClick={() => handleSelect(attachment)}
                    />
                  </li>
                ))}
              </Attachments>
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
      {selectedPetition && (
        <GeneratePetitionModal
          petition={selectedPetition}
          petitionerData={petitionerData}
          attorney={attorney}
          onClose={() => setSelectedPetition()}
        />
      )}
    </PetitionTable>
  );
}
