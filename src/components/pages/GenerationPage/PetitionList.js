import React, { useState } from 'react';
import cx from 'classnames';
import { greyScale } from '../../../styles/colors';
import Axios from '../../../service/axios';
import { TABLET_LANDSCAPE_SIZE } from '../../../styles/media';
import { Table, TableBody, TableCell, TableHeader, TableRow } from '../../elements/Table';
import useWindowSize from '../../../hooks/useWindowSize';
import { PETITION_FORM_NAMES } from '../../../constants/petitionConstants';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faDownload,
  faChevronDown,
  faBook,
  faExclamationTriangle,
} from '@fortawesome/free-solid-svg-icons';
import { Button } from '../../elements/Button';
import { usePetitionQuery } from '../../../service/api';
import { SelectAgenciesModal } from '../../../features/SelectAgencies';
import OffenseTableModal from '../../../features/OffenseTable/OffenseTableModal';
import { Tooltip } from '../../elements/Tooltip/Tooltip';
import { SelectDocumentsModal } from '../../../features/SelectDocuments';
import downloadPdf from '../../../util/downloadPdf';

function ActionButton({
  className,
  label,
  onClick,
  collapsedIcon,
  title = '',
  isDisabled = false,
  tooltipMessage = '',
  tooltipOffset = [0, 10],
}) {
  const windowSize = useWindowSize();
  const isCollapsed = windowSize.width <= TABLET_LANDSCAPE_SIZE;
  return (
    <TooltipWrapper tooltipMessage={tooltipMessage} tooltipOffset={tooltipOffset}>
      <Button
        className={cx(className, 'text-[1.55rem]')}
        onClick={onClick}
        disabled={isDisabled}
        title={title}
      >
        {isCollapsed && collapsedIcon ? <FontAwesomeIcon icon={collapsedIcon} /> : label}
      </Button>
    </TooltipWrapper>
  );
}

const TooltipWrapper = ({ children, tooltipMessage = '', tooltipOffset = [0, 10] }) => (
  <Tooltip tooltipContent={tooltipMessage} hideTooltip={!tooltipMessage} offset={tooltipOffset}>
    {children}
  </Tooltip>
);

const NO_ACTIVE_RECORDS = [
  'There are no records selected for the petition document.',
  'Please review the list of offense records and update the petition to include offense records if needed.',
];

const NO_AGENCIES_SELECTED = ['There are no agencies selected for the petition document.'];

const NO_DOCUMENTS_SELECTED = [
  'There are no documents selected for download for the petition document.',
];

function PetitionRow({ petitionData, validateInput, backgroundColor, setFormErrors }) {
  const [error, setError] = useState('');
  const { data: petition } = usePetitionQuery({ petitionId: petitionData.pk });
  const [prevPetition, setPrevPetition] = useState(petition);
  const [isOffenseModalOpen, setIsOffenseModalOpen] = useState(false);
  const [isAgencySelectModalOpen, setIsAgencySelectModalOpen] = useState(false);
  const [isSelectDocumentsOpen, setIsSelectDocumentsOpen] = useState(false);

  const allDocuments = petition ? [petition.base_document, ...(petition.attachments ?? [])] : [];
  const [selectedDocuments, setSelectedDocuments] = useState(allDocuments.map(({ pk }) => pk));
  if (petition !== prevPetition) {
    setSelectedDocuments(allDocuments.map(({ pk }) => pk));
    setPrevPetition(petition);
  }

  const handleGenerate = async () => {
    if (!validateInput()) {
      return;
    }
    const derivedPetition = _buildPetition();
    try {
      setError('');
      const { data, headers } = await Axios.post(
        `/petitions/${petitionData.pk}/generate_petition_pdf/`,
        derivedPetition,
        {
          responseType: 'arraybuffer',
        }
      );
      // content-disposition: 'inline; filename="petition.pdf"'
      const filename =
        headers['content-disposition']?.match(/filename="(.*)"/)?.[1] ?? 'petition.pdf';
      // TODO: Figure out RTK Query non-serializable ArrayBuffer issue?
      // Note: might not be worthwhile because RTK Query expects to handle only serializable response data
      // const data = await generatePetition(derivedPetition).unwrap();
      downloadPdf(data, filename);
    } catch (e) {
      if (e?.response?.data) {
        const errorData = await JSON.parse(new TextDecoder().decode(e.response.data));
        const { attorney: attorneyError, name, address1, city, state, zipcode } = errorData;
        setFormErrors((prevErrors) => ({
          ...prevErrors,
          attorney: attorneyError,
          name,
          address1,
          city,
          state,
          zipcode,
        }));
        return;
      }
      setError(!e?.response && e?.message ? e?.message : 'An unexpected error occurred');
    }
  };

  if (!petition) {
    return null;
  }

  const _buildPetition = () => ({
    documents: selectedDocuments,
  });

  const getDisabledMessage = () => {
    if (petition.active_records.length === 0) {
      const message = [...NO_ACTIVE_RECORDS];
      if (petition.form_type === 'AOC-CR-293') {
        message.push(
          'AOC-CR-293: Additional verification is needed to include offense records in this petition form'
        );
      }
      return message;
    }
    if (petition.agencies.length === 0) {
      return NO_AGENCIES_SELECTED;
    }
    if (selectedDocuments.length === 0) {
      return NO_DOCUMENTS_SELECTED;
    }
    return null;
  };

  const disabledReason = getDisabledMessage();
  const disabledTooltipContent = (
    <div className="flex flex-col gap-2">
      {disabledReason?.map((line) => <span key={line}>{line}</span>) || error}
    </div>
  );
  const areALlDocumentsSelected = selectedDocuments.length === allDocuments.length;
  return (
    <>
      <TableRow key={petition.pk} backgroundColor={backgroundColor}>
        <TableCell>{petition.county}</TableCell>
        <TableCell>{petition.jurisdiction}</TableCell>
        <TableCell>
          <TooltipWrapper tooltipMessage={PETITION_FORM_NAMES[petition.form_type]}>
            <div className="w-max border-b border-gray-700">{petition.form_type}</div>
          </TooltipWrapper>
        </TableCell>

        <TableCell>
          <ActionButton
            className="w-[100px]"
            label={`${petition.agencies.length} Agencies`}
            isCollapsed={<FontAwesomeIcon icon={faChevronDown} />}
            onClick={() => setIsAgencySelectModalOpen(true)}
            title="View/modify agencies"
          />
        </TableCell>
        <TableCell>
          <ActionButton
            label={`${petition.active_records.length} Offense${
              petition.active_records.length === 1 ? '' : 's'
            }`}
            className="w-[105px]"
            isCollapsed={<FontAwesomeIcon icon={faChevronDown} />}
            onClick={() => setIsOffenseModalOpen(true)}
            title="View/modify offense records"
          />
        </TableCell>
        <TableCell>
          {/* TODO: Add a flag icon when agencies are not added or underaged convictions are present */}
          <ActionButton
            className="w-[120px]"
            label={
              areALlDocumentsSelected
                ? `${allDocuments.length} Document${allDocuments.length === 1 ? '' : 's'}`
                : `${selectedDocuments.length}/${allDocuments.length} Selected`
            }
            onClick={() => setIsSelectDocumentsOpen(true)}
            title="Select documents for download"
          />
        </TableCell>
        <TableCell>
          <div className="flex justify-end items-center h-full gap-4 ">
            <Tooltip
              tooltipContent={disabledTooltipContent}
              hideTooltip={!disabledReason && !error}
            >
              <FontAwesomeIcon
                className={cx('text-[24px] text-red', { invisible: !disabledReason && !error })}
                icon={faExclamationTriangle}
              />
            </Tooltip>
            <button
              type="button"
              onClick={() => handleGenerate(petition)}
              disabled={!!disabledReason}
            >
              <FontAwesomeIcon
                title="Download Documents"
                icon={faDownload}
                className={cx('text-[24px]', {
                  'text-blue-primary': !disabledReason,
                  'text-gray': !!disabledReason,
                })}
              />
            </button>
          </div>
        </TableCell>
      </TableRow>
      <OffenseTableModal
        petitionId={petition.pk}
        isOpen={isOffenseModalOpen}
        onClose={() => setIsOffenseModalOpen(false)}
      />
      <SelectAgenciesModal
        petitionId={petition.pk}
        isOpen={isAgencySelectModalOpen}
        onClose={() => setIsAgencySelectModalOpen(false)}
      />
      <SelectDocumentsModal
        petitionId={petition.pk}
        documents={allDocuments}
        selectedDocuments={selectedDocuments}
        hasExistingDocuments={false}
        onAddDocument={(newPk) => setSelectedDocuments((prevList) => [...prevList, newPk])}
        onRemoveDocument={(removePk) =>
          setSelectedDocuments((prevList) => prevList.filter((pk) => pk !== removePk))
        }
        isOpen={isSelectDocumentsOpen}
        onClose={() => setIsSelectDocumentsOpen(false)}
      />
    </>
  );
}

export default function PetitionList({ petitions, validateInput, setFormErrors }) {
  return (
    <Table className="text-[1.7rem]" columnSizes="4fr 4fr 3fr 3fr 3fr 3fr 2fr">
      <TableHeader>
        <TableCell header>County</TableCell>
        <TableCell header>Jurisdiction</TableCell>
        <TableCell header>Form</TableCell>
        <TableCell tooltip="Arresting Agencies" header>
          Agencies
        </TableCell>
        <TableCell header>Offenses</TableCell>
        <TableCell header>Documents</TableCell>
        <TableCell header />
      </TableHeader>
      <TableBody>
        {petitions.map((petition, index) => (
          <PetitionRow
            key={petition.pk}
            petitionData={petition}
            validateInput={validateInput}
            backgroundColor={index % 2 === 0 ? 'white' : greyScale(9)}
            setFormErrors={setFormErrors}
          />
        ))}
      </TableBody>
    </Table>
  );
}
