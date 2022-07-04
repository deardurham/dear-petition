import React, { useState } from 'react';
import styled from 'styled-components';
import cx from 'classnames';
import { greyScale } from '../../../styles/colors';
import GeneratePetitionModal from './GeneratePetitionModal/GeneratePetitionModal';
import { TABLET_LANDSCAPE_SIZE } from '../../../styles/media';
import { Table, TableBody, TableCell, TableHeader, TableRow } from '../../elements/Table';
import StyledDialog from '../../elements/Modal/Dialog';
import Modal from '../../elements/Modal/Modal';
import useWindowSize from '../../../hooks/useWindowSize';
import { PETITION_FORM_NAMES } from '../../../constants/petitionConstants';
import AgencyAutocomplete from './GenerationInput/AgencyAutocomplete';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faDownload, faChevronDown } from '@fortawesome/free-solid-svg-icons';
import { Button } from '../../elements/Button';
import api, { usePetitionQuery } from '../../../service/api';
import Axios from '../../../service/axios';
import { useDispatch } from 'react-redux';

import OffenseTableModal from '../../../features/OffenseTable/OffenseTableModal';
import { Tooltip } from '../../elements/Tooltip/Tooltip';

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
  className,
  label,
  windowWidth,
  onClick,
  collapsedIcon,
  title = '',
  isDisabled = false,
  tooltipMessage = '',
  tooltipOffset = [0, 10],
}) {
  const isCollapsed = windowWidth <= TABLET_LANDSCAPE_SIZE;
  return (
    <Tooltip tooltipContent={tooltipMessage} hideTooltip={!tooltipMessage} offset={tooltipOffset}>
      <Button
        className={cx(className, 'text-[1.55rem]')}
        onClick={onClick}
        disabled={isDisabled}
        title={title}
      >
        {isCollapsed && collapsedIcon ? <FontAwesomeIcon icon={collapsedIcon} /> : label}
      </Button>
    </Tooltip>
  );
}

const DISABLED_MESSAGE = [
  'There are no records selected for the petition document.',
  'Please review the list of offense records and update the petition to include offense records if needed.',
];

function PetitionRow({ attorney, petitionData, petitionerData, validateInput, backgroundColor }) {
  const dispatch = useDispatch();
  const { data: petition } = usePetitionQuery({ petitionId: petitionData.pk });
  const [agencies, setAgencies] = useState([]);
  const [attachmentNumber, setAttachmentNumber] = useState();
  const [selectedPetition, setSelectedPetition] = useState();
  const windowSize = useWindowSize();
  const [isOffenseModalOpen, setIsOffenseModalOpen] = useState(false);
  const [isAgenciesDetailed, setIsAgenciesDetailed] = useState();

  const [offenseRecords, setOffenseRecords] = useState();
  const [offenseRecordsLoading, setOffenseRecordsLoading] = useState(false);
  const [highlightedRows, setHighlightedRows] = useState();
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

  if (!petition) {
    return null;
  }

  const fetchData = () => {
    setOffenseRecordsLoading(true);
    Axios.get(`/petitions/${petitionId}/`).then(({ data }) => {
      setOffenseRecords(data.offense_records);
      setHighlightedRows(data.active_records);
      setAgencies(data.agencies);
      setOffenseRecordsLoading(false);
    });
  };

  const handleAgenciesPress = () => {
    setIsAgenciesDetailed(!isAgenciesDetailed);
    if (!agencies.length) {
      fetchData();
    }
  };

  const highlightRow = (offenseRecordId) => {
    setHighlightedRows([...highlightedRows, offenseRecordId]);
  };

  const disabledMessageLines = [PETITION_FORM_NAMES[petition.form_type], ...DISABLED_MESSAGE];
  if (petition.form_type === 'AOC-CR-293') {
    disabledMessageLines.push(
      'AOC-CR-293: Additional verification is needed to include offense records in this petition form'
    );
  }
  const disabledMessage = (
    <div className="flex flex-col gap-4 p-4">
      {disabledMessageLines.map((str, i) => (
        <span key={i}>{str}</span>
      ))}
    </div>
  );

  const formName = <span className="px-4 py-2">{PETITION_FORM_NAMES[petition.form_type]}</span>;

  const isDisabled = petition.active_records.length === 0;

  const assignAgenciesToDocuments = () => {
    Axios.post(`/petitions/${petitionId}/assign_agencies_to_documents/`, {
      agencies,
    }).then(({ data }) => {
      dispatch(api.util.invalidateTags([{ type: 'Petition', id: petitionId }]));
      setAgencies(data.agencies);
    });
  };

  const petitionerDOB = offenseRecords?.find((record) => !!record?.dob)?.dob;

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
            onClick={() => handleSelect(petition.base_document)}
            isDisabled={isDisabled}
            tooltipMessage={isDisabled ? disabledMessage : formName}
            tooltipOffset={!isDisabled ? [-35, 10] : undefined}
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
            label="View"
            isCollapsed={<FontAwesomeIcon icon={faChevronDown} />}
            onClick={() => setIsOffenseModalOpen(true)}
            title="View/Modify offense records"
          />
        </TableCell>
        <TableCell>
          <GenerateButton
            label="View"
            isCollapsed={<FontAwesomeIcon icon={faChevronDown} />}
            onClick={() => handleAgenciesPress()}
            title="Reveal agencies"
          />
        </TableCell>
      </TableRow>
      <OffenseTableModal
        petitionId={petition.pk}
        isOpen={isOffenseModalOpen}
        onClose={() => setIsOffenseModalOpen(false)}
      />
      {isAgenciesDetailed && (
        <StyledDialog isOpen={isAgenciesDetailed} onClose={() => setIsAgenciesDetailed(false)}>
          {offenseRecordsLoading ? (
            <h5>Loading...</h5>
          ) : (
            <div className="w-[900px] h-auto p-10 flex flex-col gap-8">
              <h3>View / Select Agencies</h3>
              <p className="text-[1.6rem]">
                Please select or de-select agencies here if you wish to include or exclude them from
                the petition.
              </p>
              <AgencyAutocomplete
                agencies={agencies}
                setAgencies={setAgencies}
                isModified={isModified}
                setIsModified={setIsModified}
              />
              <div className="self-center flex gap-8">
                <GenerateButton
                  className="w-[15rem]"
                  label="Update Agencies"
                  onClick={assignAgenciesToDocuments}
                  title="Update the petitions on the main petition row with your changes."
                  isDisabled={!isModified}
                />
                <Button className="px-4" onClick={() => setIsAgenciesDetailed(false)}>
                  Close
                </Button>
              </div>
            </div>
          )}
        </StyledDialog>
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
    <PetitionTable numColumns={6}>
      <TableHeader>
        <TableCell header>County</TableCell>
        <TableCell header>Jurisdiction</TableCell>
        <TableCell header>Petition</TableCell>
        <TableCell header>Attachments</TableCell>
        <TableCell header>Offenses</TableCell>
        <TableCell header>Agencies</TableCell>
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
