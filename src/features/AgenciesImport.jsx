import cx from 'classnames';
import { useEffect, useRef, useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCheck, faTimes } from '@fortawesome/free-solid-svg-icons';
import { useImportAgenciesMutation, usePreviewImportAgenciesMutation } from '../service/api';
import DragNDrop from '../components/elements/DragNDrop/DragNDrop';
import { Button } from '../components/elements/Button';
import { Spinner } from '../components/elements/Spinner';
import { Table, TableHeader, HeaderCell, TableCell, TableRow } from '../components/elements/Table';
import { useModalContext } from '../components/elements/Button/ModalButton';
import { NEUTRAL } from '../components/elements/Button/Button';

// xls, xlsx
const ALLOWED_MIME_TYPES = [
  'application/vnd.ms-excel',
  'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
];

const ImportErrors = ({ errors, file, onClearFile }) => {
  const [triggerPreviewImport, { isLoading: isSubmitting }] = usePreviewImportAgenciesMutation({
    fixedCacheKey: file?.name,
  });
  return (
    <div className="p-6 flex flex-col gap-4 w-[800px] h-[500px]">
      <h3 className="text-red">Error: Unable to Import</h3>
      <Table className="flex-1 grid grid-cols-[60px_1fr] max-h-[500px] overflow-auto h-full auto-rows-max">
        <TableHeader>
          <HeaderCell>Row</HeaderCell>
          <HeaderCell>Error</HeaderCell>
        </TableHeader>
        {Object.entries(errors).map(([rowNumber, rowErrors]) => (
          <TableRow key={rowNumber}>
            <TableCell>{rowNumber}</TableCell>
            <TableCell className="whitespace-normal">{rowErrors.join('\n')}</TableCell>
          </TableRow>
        ))}
      </Table>
      <div className="flex items-start gap-2">
        <Button disabled={!file} className="px-4" colorClass={NEUTRAL} onClick={() => onClearFile()}>
          Select New File
        </Button>
        <Button
          disabled={!file}
          className="px-4"
          onClick={() => {
            const formData = new FormData();
            formData.append('file', file);
            triggerPreviewImport({ data: formData });
          }}
        >
          Resubmit
        </Button>
        {isSubmitting && <Spinner />}
      </div>
    </div>
  );
};

const ImportPreview = ({ rowDiffs, file }) => {
  const [triggerImport] = useImportAgenciesMutation();
  const { closeModal } = useModalContext();
  if (rowDiffs.length === 0) {
    return (
      <div className="p-6 flex flex-col gap-4 h-full">
        <h3>Preview Changes</h3>
        <p>No changes detected in submitted spreadsheet.</p>
      </div>
    );
  }
  return (
    <div className="p-6 flex flex-col gap-4 w-[900px] h-[500px]">
      <h3>Preview Changes</h3>
      <Table className="flex-1 grid grid-cols-[2fr_2fr_1fr_60px_1fr_1fr_80px] max-h-[500px] overflow-auto h-full auto-rows-max">
        <TableHeader>
          <HeaderCell>Arresting Agency</HeaderCell>
          <HeaderCell>Address</HeaderCell>
          <HeaderCell>City</HeaderCell>
          <HeaderCell>State</HeaderCell>
          <HeaderCell>Zipcode</HeaderCell>
          <HeaderCell>County</HeaderCell>
          <HeaderCell>Sheriff?</HeaderCell>
        </TableHeader>
        {rowDiffs.map(({ new_fields, name, address, city, state, zipcode, county, is_sheriff }) => (
          <TableRow key={name}>
            <TableCell className={cx({ 'bg-green': new_fields.includes('name') })}>{name}</TableCell>
            <TableCell className={cx({ 'bg-green': new_fields.includes('address') })}>{address}</TableCell>
            <TableCell className={cx({ 'bg-green': new_fields.includes('city') })}>{city}</TableCell>
            <TableCell className={cx({ 'bg-green': new_fields.includes('state') })}>{state}</TableCell>
            <TableCell className={cx({ 'bg-green': new_fields.includes('zipcode') })}>{zipcode}</TableCell>
            <TableCell className={cx({ 'bg-green': new_fields.includes('county') })}>{county}</TableCell>
            <TableCell className={cx({ 'bg-green': new_fields.includes('is_sheriff') })}>
              <FontAwesomeIcon icon={is_sheriff ? faCheck : faTimes} />
            </TableCell>
          </TableRow>
        ))}
      </Table>
      <div className="flex gap-2">
        <Button
          onClick={async () => {
            const formData = new FormData();
            formData.append('file', file);
            await triggerImport({ data: formData }).unwrap();
            closeModal();
          }}
        >
          Accept Changes
        </Button>
        <Button onClick={() => closeModal()}>Cancel</Button>
      </div>
    </div>
  );
};

const AgenciesFileSelect = ({ file, onSetFile }) => {
  const fileInputRef = useRef();
  const [triggerPreviewImport, { isLoading: isSubmitting }] = usePreviewImportAgenciesMutation({
    fixedCacheKey: file?.name,
  });

  const message = !file ? 'Drag and Drop files here or click to open file finder' : `Selection: ${file.name}`;
  return (
    <div className="flex flex-col gap-6 p-6">
      <h2 className="mb-2">Upload Agency Spreadsheet</h2>
      <DragNDrop
        className="max-w-[360px] min-h-[125px] p-8"
        ref={fileInputRef}
        mimeTypes={ALLOWED_MIME_TYPES}
        maxFiles={1}
        onDrop={(drop) => onSetFile(drop?.files?.[0])}
      >
        <span className="whitespace-normal">{message}</span>
      </DragNDrop>
      <div className="flex items-start gap-2">
        <Button
          disabled={!file}
          className="px-4"
          onClick={() => {
            const formData = new FormData();
            formData.append('file', file);
            triggerPreviewImport({ data: formData });
          }}
        >
          Submit
        </Button>
        {isSubmitting && <Spinner />}
      </div>
    </div>
  );
};

const AgenciesImport = () => {
  const [file, setFile] = useState();
  const [previewResult, setPreviewResult] = useState();
  const [_triggerPreview, { data, reset }] = usePreviewImportAgenciesMutation({
    fixedCacheKey: file?.name,
  });

  useEffect(() => {
    return () => {
      reset();
    };
  }, [reset]);

  if (data && previewResult !== data) {
    setPreviewResult(data);
  }

  if (!previewResult) {
    return <AgenciesFileSelect file={file} onSetFile={(file) => setFile(file)} onClose={() => reset()} />;
  } else if (previewResult.has_errors) {
    return (
      <ImportErrors
        errors={previewResult.row_errors}
        file={file}
        onClearFile={() => {
          reset();
          setPreviewResult(null);
        }}
      />
    );
  }
  return <ImportPreview rowDiffs={previewResult.row_diffs} file={file} />;
};

export const AgenciesImportModal = () => (
  <div className="max-w-[1200px] max-h-[500px] bg-white">
    <AgenciesImport />
  </div>
);
