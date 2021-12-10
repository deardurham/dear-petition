import React, { useState } from 'react';
import styled from 'styled-components';
import { Button } from '../../elements/Button';
import { greyScale } from '../../../styles/colors';
import Axios from '../../../service/axios';
import GeneratePetitionModal from './GeneratePetitionModal/GeneratePetitionModal';
import { TABLET_LANDSCAPE_SIZE } from '../../../styles/media';
import {
  Table,
  TableBody,
  TableCell,
  TableSpanCell,
  TableHeader,
  TableRow,
} from '../../elements/Table';
import useWindowSize from '../../../hooks/useWindowSize';
import HighlightTable from '../../elements/HighlightTable/HighlightTable';
import { PETITION_FORM_NAMES } from '../../../constants/petitionConstants';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faDownload, faChevronRight, faChevronDown } from '@fortawesome/free-solid-svg-icons';

const GenerateButtonStyled = styled(Button)`
  font-size: 1.5rem;
  opacity: ${(props) => (props.disabled ? 0.3 : 1)};
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

function GenerateButton({
  label,
  windowWidth,
  onClick,
  collapsedIcon,
  title = '',
  isDisabled = false,
}) {
  const isCollapsed = windowWidth <= TABLET_LANDSCAPE_SIZE;
  return (
    <GenerateButtonStyled onClick={onClick} disabled={isDisabled} title={title}>
      {isCollapsed && collapsedIcon ? <FontAwesomeIcon icon={collapsedIcon} /> : label}
    </GenerateButtonStyled>
  );
}

function PetitionRow({ attorney, petitionData, petitionerData, validateInput, backgroundColor }) {
  const [agencies, setAgencies] = useState([]);
  const [attachmentNumber, setAttachmentNumber] = useState();
  const [selectedPetition, setSelectedPetition] = useState();
  const windowSize = useWindowSize();
  const [isDetailed, setIsDetailed] = useState();

  const [offenseRecords, setOffenseRecords] = useState();
  const [offenseRecordsLoading, setOffenseRecordsLoading] = useState(false);
  const [petition, setPetition] = useState(petitionData);
  const [highlightedRows, setHighlightedRows] = useState();
  const [isDisabled, setIsDisabled] = useState(petition.form_type === 'AOC-CR-293');
  const [isModified, setIsModified] = useState(false);
  const petitionId = petition.pk;

  const handleSelect = (newPetition, num) => {
    if (validateInput()) {
      setSelectedPetition(newPetition);
      if (num) {
        setAttachmentNumber(num);
      }
    }
  };

  const handlePress = () => {
    setIsDetailed(!isDetailed);
    if (!offenseRecords) {
      setOffenseRecordsLoading(true);
      Axios.get(`/petitions/${petitionId}/`).then(({ data }) => {
        setOffenseRecords(data.offense_records);
        setHighlightedRows(data.active_records);
        setOffenseRecordsLoading(false);
      });
    }
  };

  const highlightRow = (offenseRecordId) => {
    setHighlightedRows([...highlightedRows, offenseRecordId]);
  };

  const unhighlightRow = (offenseRecordId) => {
    setHighlightedRows(highlightedRows.filter((value) => value !== offenseRecordId));
  };

  const recalculatePetitions = () => {
    Axios.post(`/petitions/${petitionId}/recalculate_petitions/`, {
      offense_record_ids: highlightedRows,
    }).then(({ data }) => {
      setPetition(data);
      setIsDetailed(false);
      setIsDisabled(false);
    });
  };

  return (
    <>
      <TableRow key={petition.pk} backgroundColor={backgroundColor}>
        <TableCell>{petition.county}</TableCell>
        <TableCell>{petition.jurisdiction}</TableCell>
        <TableCell>
          <GenerateButton
            collapsedIcon={faDownload}
            windowWidth={windowSize.width}
            label={petition.form_type}
            onClick={() => handleSelect(petition)}
            isDisabled={isDisabled}
            title={PETITION_FORM_NAMES[petition.form_type]}
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
        <TableCell>
          <GenerateButton
            label={
              isDetailed ? (
                <FontAwesomeIcon icon={faChevronDown} />
              ) : (
                <FontAwesomeIcon icon={faChevronRight} />
              )
            }
            isCollapsed={<FontAwesomeIcon icon={faChevronDown} />}
            onClick={() => handlePress()}
            title="Reveal offense records"
          />
        </TableCell>
      </TableRow>
      {isDetailed && (
        <TableRow backgroundColor={backgroundColor}>
          <TableSpanCell spanLength={5}>
            {offenseRecordsLoading ? (
              <h5>Loading...</h5>
            ) : (
              <Table>
                <TableBody>
                  <TableRow>
                    <TableCell>
                      <HighlightTable
                        offenseRecords={offenseRecords}
                        highlightRow={highlightRow}
                        highlightedRows={highlightedRows}
                        unhighlightRow={unhighlightRow}
                        setIsModified={setIsModified}
                      />
                    </TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell>
                      <GenerateButton
                        label="Update Petitions"
                        onClick={recalculatePetitions}
                        title="Update the petitions on the main petition row with your changes."
                        isDisabled={!isModified}
                      />
                    </TableCell>
                  </TableRow>
                </TableBody>
              </Table>
            )}
          </TableSpanCell>
        </TableRow>
      )}
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
    <PetitionTable numColumns={5}>
      <TableHeader>
        <TableCell header>County</TableCell>
        <TableCell header>Jurisdiction</TableCell>
        <TableCell header>Petition</TableCell>
        <TableCell header>Attachments</TableCell>
        <TableCell header>Detail</TableCell>
      </TableHeader>
      <TableBody>
        {petitions.map((petition, index) => (
          <PetitionRow
            key={petition.pk}
            petitionData={petition}
            petitionerData={petitionerData}
            attorney={attorney}
            validateInput={validateInput}
            backgroundColor={index % 2 === 0 ? 'white' : greyScale(9)}
          />
        ))}
      </TableBody>
    </PetitionTable>
  );
}
