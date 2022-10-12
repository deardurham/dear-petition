import React from 'react';
import { usePetitionQuery } from '../service/api';
import StyledDialog from '../components/elements/Modal/Dialog';
import { Table, TableBody, TableCell, TableHeader, TableRow } from '../components/elements/Table';

export const SelectDocumentsModal = ({
  isOpen,
  onAddDocument,
  onRemoveDocument,
  onClose,
  petitionId,
  documents,
  selectedDocuments,
}) => {
  const test = 0;
  return (
    <StyledDialog isOpen={isOpen} onClose={() => onClose()}>
      <div className="w-[400px] h-[200px] flex flex-col">
        <SelectDocuments
          petitionId={petitionId}
          onAddDocument={onAddDocument}
          onRemoveDocument={onRemoveDocument}
          onClose={onClose}
          documents={documents}
          selectedDocuments={selectedDocuments}
        />
      </div>
    </StyledDialog>
  );
};

const SelectDocuments = ({
  petitionId,
  onAddDocument,
  onRemoveDocument,
  onClose,
  documents,
  selectedDocuments,
}) => {
  const { data: petition } = usePetitionQuery({ petitionId });
  return (
    <div className="px-4 py-2">
      <p>Select documents for downloading</p>
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
    </div>
  );
};
