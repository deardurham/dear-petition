import React, { useState } from 'react';
import styled from 'styled-components';
import { Button } from '../../elements/Button/Button.styled';
import GeneratePetitionModal from './GeneratePetitionModal/GeneratePetitionModal';
import { TABLET_LANDSCAPE_SIZE } from '../../../styles/media';
import { Table, TableRow, TableCell } from '../../elements/Table';
import useWindowSize from '../../../hooks/useWindowSize';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faDownload } from '@fortawesome/free-solid-svg-icons';

const GenerateButtonStyled = styled(Button)`
  font-size: 1.4rem;
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

export default function PetitionList({ petitions, attorney, petitionerData, onError }) {
  const [selectedPetition, setSelectedPetition] = useState();
  const windowSize = useWindowSize();

  const handleSelect = (petition) => {
    let hasErrors = false;
    if (!attorney) {
      onError({ attorney: ['Please select an attorney from the list'] });
      hasErrors = true;
    }
    for (const key of ['petitionerName', 'ssn', 'licenseNumber', 'licenseState']) {
      if (!petitionerData[key]) {
        onError({ [key]: ['This field is required'] });
        hasErrors = true;
      }
    }
    for (const key of ['address1', 'city', 'state', 'zipCode']) {
      if (!petitionerData.address[key]) {
        onError({ [key]: ['This field is required'] });
        hasErrors = true;
      }
    }
    if (!hasErrors) {
      setSelectedPetition(petition);
    }
  }

  return (
    <Table numColumns={4} headers={['County', 'Jurisdiction', 'Primary Form', 'Attachments']}>
      {petitions.map(petition => (
        <TableRow key={petition.pk}>
          <TableCell>{`${petition.county} County`}</TableCell>
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
                    <span>{`${i+1}) `}</span>
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
      {selectedPetition && (
        <GeneratePetitionModal
          petition={selectedPetition}
          petitionerData={petitionerData}
          attorney={attorney}
          onClose={() => setSelectedPetition()}
        />
      )}
    </Table>
  );
}
