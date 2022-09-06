import React, { useState } from 'react';
import styled from 'styled-components';
import cx from 'classnames';
import { greyScale } from '../../../styles/colors';
import GeneratePetitionModal from './GeneratePetitionModal/GeneratePetitionModal';
import { TABLET_LANDSCAPE_SIZE } from '../../../styles/media';
import { Table, TableBody, TableCell, TableHeader, TableRow } from '../../elements/Table';
import useWindowSize from '../../../hooks/useWindowSize';
import { PETITION_FORM_NAMES } from '../../../constants/petitionConstants';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faDownload, faChevronDown } from '@fortawesome/free-solid-svg-icons';
import { Button } from '../../elements/Button';
import { usePetitionQuery } from '../../../service/api';
import { SelectAgenciesModal } from '../../../features/SelectAgencies';
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
  const { data: petition } = usePetitionQuery({ petitionId: petitionData.pk });
  const [agencies, setAgencies] = useState([]);
  const [attachmentNumber, setAttachmentNumber] = useState();
  const [selectedPetition, setSelectedPetition] = useState();
  const windowSize = useWindowSize();
  const [isOffenseModalOpen, setIsOffenseModalOpen] = useState(false);
  const [isAgencySelectModalOpen, setIsAgencySelectModalOpen] = useState(false);

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
            label="View/Modify"
            isCollapsed={<FontAwesomeIcon icon={faChevronDown} />}
            onClick={() => setIsOffenseModalOpen(true)}
            title="View/Modify offense records"
          />
        </TableCell>
        <TableCell>
          <GenerateButton
            label="View/Modify"
            isCollapsed={<FontAwesomeIcon icon={faChevronDown} />}
            onClick={() => setIsAgencySelectModalOpen(true)}
            title="Reveal agencies"
          />
        </TableCell>
      </TableRow>
      <OffenseTableModal
        petitionId={petition.pk}
        isOpen={isOffenseModalOpen}
        onClose={() => setIsOffenseModalOpen(false)}
      />
      <SelectAgenciesModal
        isOpen={isAgencySelectModalOpen}
        onClose={() => setIsAgencySelectModalOpen(false)}
      />
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
