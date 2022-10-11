import React, { useState } from 'react';
import styled from 'styled-components';
import cx from 'classnames';
import { greyScale } from '../../../styles/colors';
import Axios from '../../../service/axios';
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
import { cleanFilename } from '../../../util/file';

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

const DISABLED_MESSAGE = [
  'There are no records selected for the petition document.',
  'Please review the list of offense records and update the petition to include offense records if needed.',
];

function PetitionRow({ attorney, petitionData, petitionerData, validateInput, backgroundColor }) {
  const [pdfWindow, setPdfWindow] = useState({ handle: null, url: null });
  const [error, setError] = useState('');
  const { data: petition } = usePetitionQuery({ petitionId: petitionData.pk });
  const [isOffenseModalOpen, setIsOffenseModalOpen] = useState(false);
  const [isAgencySelectModalOpen, setIsAgencySelectModalOpen] = useState(false);

  const _openPdf = (pdf) => {
    const pdfBlob = new Blob([pdf], { type: 'application/pdf' });

    // IE doesn't allow using a blob object directly as link href
    // instead it is necessary to use msSaveOrOpenBlob
    if (window.navigator && window.navigator.msSaveOrOpenBlob) {
      window.navigator.msSaveOrOpenBlob(pdfBlob);
      return;
    }

    // Clean up previous pdf when generating new one
    const { handle: oldHandle, url: oldUrl } = pdfWindow;
    if (oldUrl) window.URL.revokeObjectURL(oldUrl);
    if (oldHandle) oldHandle.close();

    const url = window.URL.createObjectURL(pdfBlob);
    setPdfWindow({ handle: window.open(url), url });
  };

  const downloadPdf = (pdf, filename) => {
    const pdfBlob = new Blob([pdf], { type: 'application/pdf' });
    const url = window.URL.createObjectURL(pdfBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    link.click();
    setTimeout(() => {
      window.URL.revokeObjectURL(url);
      link.remove();
    });
  };

  const closePdf = () => {
    const { url, handle } = pdfWindow;
    if (url) window.URL.revokeObjectURL(url);
    if (handle) handle.close();

    setPdfWindow({ handle: null, url: null });
  };

  const handleGenerate = async () => {
    if (!validateInput()) {
      return;
    }
    const derivedPetition = _buildPetition();
    try {
      setError('');
      const { data, headers } = await Axios.post(
        `/petitions/${petition.pk}/generate_petition_pdf/`,
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
      setError(!e?.response && e?.message ? e?.message : 'An unexpected error occurred');
    }
  };

  if (!petition) {
    return null;
  }

  const _buildPetition = () => ({
    documents: [petition.base_document.pk, ...petition.attachments.map(({ pk }) => pk)],
    name_petitioner: petitionerData.name,
    address1: petitionerData.address1,
    address2: petitionerData.address2,
    city: petitionerData.city,
    state: petitionerData.state.value,
    zip_code: petitionerData.zipCode,
    attorney: attorney.value,
    agencies: petition.agencies.map((agency) => agency.pk),
  });

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
          <TooltipWrapper tooltipMessage={PETITION_FORM_NAMES[petition.form_type]}>
            <div className="w-max border-b border-gray-700">{petition.form_type}</div>
          </TooltipWrapper>
        </TableCell>
        <TableCell>
          {/* TODO: Options menu allows selection of "Download all", "Download Selected", and "Preview" */}
          {/* TODO: Add separate "Generate" button */}
          <ActionButton
            collapsedIcon={faDownload}
            label={petition.form_type}
            onClick={() => handleGenerate(petition)}
            isDisabled={isDisabled}
            tooltipMessage={isDisabled ? disabledMessage : formName}
          />
        </TableCell>
        <TableCell>
          <ActionButton
            label="View/Modify"
            isCollapsed={<FontAwesomeIcon icon={faChevronDown} />}
            onClick={() => setIsOffenseModalOpen(true)}
            title="View/Modify offense records"
          />
        </TableCell>
        <TableCell>
          <ActionButton
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
    </>
  );
}

export default function PetitionList({ attorney, petitions, petitionerData, validateInput }) {
  return (
    <PetitionTable numColumns={6}>
      <TableHeader>
        <TableCell header>County</TableCell>
        <TableCell header>Jurisdiction</TableCell>
        <TableCell header>Form</TableCell>
        <TableCell header>Documents</TableCell>
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
