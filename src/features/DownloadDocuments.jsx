import React, { useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import cx from 'classnames';
import StyledDialog from '../components/elements/Modal/Dialog';
import { Table, TableBody, TableCell, TableHeader, TableRow } from '../components/elements/Table';
import Button from '../components/elements/Button';
import { POSITIVE } from '../components/elements/Button/Button';
import { downloadPdf } from '../util/downloadFile';
import { manualAxiosRequest } from '../service/axios';
import { getErrorList, hasValidationsErrors } from '../util/errors';
import { Tooltip } from '../components/elements/Tooltip/Tooltip';
import { faExclamationTriangle } from '@fortawesome/free-solid-svg-icons';

export const DownloadDocumentsModal = ({ isOpen, onClose, petitions }) => (
  <StyledDialog isOpen={isOpen} onClose={() => onClose()}>
    <div className="w-[600px] max-h-[500px] p-10 flex flex-col gap-8">
      <h3>Select Documents for Download</h3>
      <p className="text-[1.6rem]">Please select or de-select documents here for download.</p>
      <DownloadExistingDocuments petitions={petitions} />

      <div className="p-10 flex flex-row justify-center gap-8">
        <Button
          type="button"
          colorClass={POSITIVE}
          className="px-4 py-2 self-center"
          onClick={() => onClose()}
        >
          Close
        </Button>
      </div>
    </div>
  </StyledDialog>
);

const handleDownload = async (petition) => {
  const { pk, documents } = petition;
  const { data, meta } = await manualAxiosRequest({
    url: `/petitions/${pk}/generate_petition_pdf/`,
    data: { documents },
    responseType: 'arraybuffer',
    method: 'post',
  });
  const { headers } = meta.response;
  const filename = headers['content-disposition']?.match(/filename="(.*)"/)?.[1] ?? 'petition.pdf';
  downloadPdf(data, filename);
};

const DownloadExistingDocuments = ({ petitions }) => {
  const [errors, setErrors] = useState({});
  return (
    <Table numColumns={4}>
      <TableHeader>
        <TableCell header>Form</TableCell>
        <TableCell header>Jurisdiction</TableCell>
        <TableCell header>Attachments</TableCell>
        <TableCell header />
      </TableHeader>
      <TableBody>
        {petitions.map((petition) => (
          <TableRow key={petition.pk}>
            <TableCell>{petition.form_type}</TableCell>
            <TableCell>{petition.jurisdiction}</TableCell>
            <TableCell>
              {petition.documents.length > 0 ? petition.documents.length - 1 : 0}
            </TableCell>
            <TableCell>
              <div className="flex items-center gap-2">
                <Tooltip
                  tooltipContent={errors?.[petition.pk]}
                  hideTooltip={!errors?.[petition.pk]}
                >
                  <FontAwesomeIcon
                    className={cx('text-[24px] text-red', { invisible: !errors?.[petition.pk] })}
                    icon={faExclamationTriangle}
                  />
                </Tooltip>
                <Button
                  type="button"
                  colorClass={POSITIVE}
                  className="px-4 py-2 self-center"
                  disabled={hasValidationsErrors(petition.can_generate)}
                  title={
                    hasValidationsErrors(petition.can_generate)
                      ? getErrorList(petition.can_generate?.petition ?? {}).join(' ')
                      : undefined
                  }
                  onClick={async () => {
                    setErrors({});
                    try {
                      await handleDownload(petition);
                    } catch (e) {
                      setErrors((prev) => ({
                        ...prev,
                        [petition.pk]: 'An error occurred while attempting to download.',
                      }));
                    }
                  }}
                >
                  Download
                </Button>
              </div>
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
};
