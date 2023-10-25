import cx from 'classnames';
import { useRef, useState } from 'react';
import { useImportAgenciesMutation, usePreviewImportAgenciesMutation } from '../service/api';
import DragNDrop from '../components/elements/DragNDrop/DragNDrop';
import { Button } from '../components/elements/Button';
import { Spinner } from '../components/elements/Spinner';
import { Table, TableHeader, HeaderCell, TableCell, TableRow } from '../components/elements/Table';

// xls, xlsx
const ALLOWED_MIME_TYPES = [
  'application/vnd.ms-excel',
  'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
];

const ImportErrors = ({ errors }) => {
  return (
    <div className="p-6 flex flex-col gap-4 h-full">
      <h3 className="text-red">Error: Unable to import</h3>
      <Table className="flex-1 grid grid-cols-[60px_1fr] overflow-auto h-full auto-rows-max">
        <TableHeader>
          <HeaderCell>Row</HeaderCell>
          <HeaderCell>Error</HeaderCell>
        </TableHeader>
        {Object.entries(errors).map(([rowNumber, rowErrors]) => (
          <TableRow key={rowErrors.join('\n')}>
            <TableCell>{rowNumber}</TableCell>
            <TableCell>{rowErrors.join('\n')}</TableCell>
          </TableRow>
        ))}
      </Table>
    </div>
  );
};

const ImportPreview = ({ rowDiffs }) => {
  return (
    <div className="p-6 flex flex-col gap-4 h-full">
      <h3>Preview Changes</h3>
      <Table className="flex-1 grid grid-cols-[2fr_2fr_1fr_60px_1fr_1fr] overflow-auto h-full auto-rows-max">
        <TableHeader>
          <HeaderCell>Arresting Agency</HeaderCell>
          <HeaderCell>Address</HeaderCell>
          <HeaderCell>City</HeaderCell>
          <HeaderCell>State</HeaderCell>
          <HeaderCell>Zipcode</HeaderCell>
          <HeaderCell>County</HeaderCell>
        </TableHeader>
        {rowDiffs.map(({ new_fields, name, address, city, state, zipcode, county }) => (
          <TableRow key={name}>
            <TableCell className={cx({ 'bg-green': new_fields.includes('name') })}>{name}</TableCell>
            <TableCell className={cx({ 'bg-green': new_fields.includes('address') })}>{address}</TableCell>
            <TableCell className={cx({ 'bg-green': new_fields.includes('city') })}>{city}</TableCell>
            <TableCell className={cx({ 'bg-green': new_fields.includes('state') })}>{state}</TableCell>
            <TableCell className={cx({ 'bg-green': new_fields.includes('zipcode') })}>{zipcode}</TableCell>
            <TableCell className={cx({ 'bg-green': new_fields.includes('county') })}>{county}</TableCell>
          </TableRow>
        ))}
      </Table>
    </div>
  );
};

const AgenciesImport = () => {
  const [file, setFile] = useState();
  const [_triggerPreview, { data: previewResult }] = usePreviewImportAgenciesMutation({ fixedCacheKey: file?.name });
  console.log({ previewResult });
  if (!previewResult) {
    return <AgenciesPreviewImport file={file} onSetFile={(file) => setFile(file)} />;
  } else if (previewResult.has_errors) {
    return <ImportErrors errors={previewResult.row_errors} />;
  }
  return <ImportPreview rowDiffs={previewResult.row_diffs} />;
};

const AgenciesPreviewImport = ({ file, onSetFile }) => {
  const fileInputRef = useRef();
  const [_triggerImport] = useImportAgenciesMutation();
  const [_triggerPreviewImport, { isLoading: isSubmitting }] = usePreviewImportAgenciesMutation({
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
            _triggerPreviewImport({ data: formData });
          }}
        >
          Submit
        </Button>
        {isSubmitting && <Spinner />}
      </div>
    </div>
  );
};

export const AgenciesImportModal = () => (
  <div className="w-[700px] h-[500px] bg-white">
    <AgenciesImport />
  </div>
);
