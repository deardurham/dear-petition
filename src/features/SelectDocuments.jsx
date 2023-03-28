import React from 'react';
import StyledDialog from '../components/elements/Modal/Dialog';
import { Table, TableBody, TableCell, TableHeader, TableRow } from '../components/elements/Table';
import Button from '../components/elements/Button';
import { POSITIVE } from '../components/elements/Button/Button';
import downloadPdf from '../util/downloadPdf';
import Axios from '../service/axios';

export const SelectDocumentsModal = ({
  isOpen,
  onAddDocument,
  onRemoveDocument,
  onClose,
  documents,
  hasExistingDocuments,
  selectedDocuments,
}) => (
  <StyledDialog isOpen={isOpen} onClose={() => onClose()}>
    <div className="w-[500px] max-h-[500px] p-10 flex flex-col gap-8">
      <h3>Select Documents for Download</h3>
      <p className="text-[1.6rem]">Please select or de-select documents here for download.</p>
      {hasExistingDocuments ? (
        <DownloadExistingDocuments documents={documents} />
      ) : (
        <SelectDocuments
          onAddDocument={onAddDocument}
          onRemoveDocument={onRemoveDocument}
          documents={documents}
          selectedDocuments={selectedDocuments}
        />
      )}

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

const DownloadExistingDocuments = ({ documents }) => (
  <Table columnSizes="3 1fr">
    <TableHeader>
      <TableCell header />
      <TableCell header>Form</TableCell>
    </TableHeader>
    <TableBody>
      {documents.map((document) => (
        <TableRow className="flex" key={document.pk}>
          <TableCell className="flex-grow">{document.form_type}</TableCell>
          <TableCell>
            <Button
              type="button"
              colorClass={POSITIVE}
              className="px-4 py-2 self-center"
              onClick={() => handleDownload(document)}
            >
              Download
            </Button>
          </TableCell>
        </TableRow>
      ))}
    </TableBody>
  </Table>
);

const SelectDocuments = ({ onAddDocument, onRemoveDocument, documents, selectedDocuments }) => (
  <Table columnSizes="40px 1fr">
    <TableHeader>
      <TableCell header />
      <TableCell header>Form</TableCell>
    </TableHeader>
    <TableBody>
      {documents.map((document) => (
        <TableRow key={document.pk}>
          <TableCell>
            <input
              type="checkbox"
              className="cursor-pointer"
              checked={selectedDocuments.includes(document.pk)}
              onChange={(e) =>
                e.target.checked ? onAddDocument(document.pk) : onRemoveDocument(document.pk)
              }
            />
          </TableCell>
          <TableCell>{document.form_type}</TableCell>
        </TableRow>
      ))}
    </TableBody>
  </Table>
);

const handleDownload = async (document) => {
  const { pk, documents } = document;
  try {
    const { data, headers } = await Axios.post(
      `/petitions/${pk}/generate_petition_pdf/`,
      { documents },
      {
        responseType: 'arraybuffer',
      }
    );
    const filename =
      headers['content-disposition']?.match(/filename="(.*)"/)?.[1] ?? 'petition.pdf';
    downloadPdf(data, filename);
  } catch (err) {
    console.log(err);
  }
};
