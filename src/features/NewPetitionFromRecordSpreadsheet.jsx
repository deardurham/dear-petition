import React, { useState, useEffect } from 'react';
import { useHistory } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTimes } from '@fortawesome/free-solid-svg-icons';
import { Button, CloseButton } from '../components/elements/Button';
import DragNDrop from '../components/elements/DragNDrop/DragNDrop';
import { useCreateBatchFromRecordSpreadsheetMutation } from '../service/api';
import { Spinner } from '../components/elements/Spinner';
import { POSITIVE } from '../components/elements/Button/Button';

const ALLOWED_MIME_TYPES = [
  'application/vnd.ms-excel',
  'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
];
const MAX_FILES = 1;
const LONG_WAIT_TIMEOUT = 5; // seconds

const RecordUpload = () => {
  const fileInputRef = React.createRef();
  const [dragWarnings, setDragWarnings] = useState();
  const [dragErrors, setDragErrors] = useState();
  const [uploadError, setUploadError] = useState('');
  const [files, setFiles] = useState(new Set());
  const history = useHistory();
  const [createBatch, { isLoading: isUploading }] = useCreateBatchFromRecordSpreadsheetMutation();
  const [isMounted, setIsMounted] = useState(false);

  useEffect(() => {
    setIsMounted(true);
    return () => {
      setIsMounted(false);
    };
  }, []);

  const handleDrop = (drop) => {
    setDragErrors(drop.errors);
    setDragWarnings(drop.warnings);
    if (files.size + drop.files.length > MAX_FILES) {
      setDragErrors(['Maximum file limit exceeded']);
      return;
    }
    setFiles(new Set(drop.files));
  };

  const handleRemoveFile = (file) => {
    // browser stores a "path" to the last file uploaded on the input.
    // It's necessary to "clear" the inputs value here, but not on drop--
    // the browser just replaces previous files in the case of a drop.
    if (fileInputRef.current) fileInputRef.current.value = '';
    // TODO: It would be great to get this taken care of inside DragNDrop,
    // TODO: but currently DragNDrop has no concept of a FilesList or removing files.
    const copiedSet = new Set(files);
    copiedSet.delete(file);
    setFiles(copiedSet);
  };

  const handleRecordsSpreadsheetImport = async () => {
    setUploadError(true);
    let timer = null;
    const filesFormData = new FormData();
    files.forEach((file) => filesFormData.append('files', file));
    timer = setTimeout(() => {
      if (isMounted) {
        setUploadError('It is taking longer than expected to process the uploaded records. Please wait...');
      }
    }, LONG_WAIT_TIMEOUT * 1000);

    createBatch({ data: filesFormData })
      .unwrap()
      .then((data) => {
        if (timer) {
          clearTimeout(timer);
        }
        history.push(`/generate/${data.batch_id}`);
      })
      .catch(() => {
        if (timer) {
          clearTimeout(timer);
        }
        if (isMounted) {
          setUploadError('ERROR: Could not process the records.');
        }
      });
  };

  const hasFiles = files?.size > 0 ?? false;

  return (
    <>
      <DragNDrop
        className="max-w-[360px] min-h-[125px]"
        ref={fileInputRef}
        mimeTypes={ALLOWED_MIME_TYPES}
        maxFiles={MAX_FILES}
        onDrop={handleDrop}
      >
        <div className="flex flex-col justify-between items-center gap-4 px-3 py-10">
          <div className="">
            <h2>Upload Record Spreadsheet</h2>
            <p className="whitespace-normal">Drag and Drop files here or click to open file finder</p>
          </div>
          <div className="flex flex-col gap-4 self-start">
            {dragWarnings && (
              <div className="flex flex-col gap-2">
                {dragWarnings.map((warning) => (
                  <p key={warning} className="text-yellow">
                    {`Warning: ${warning}`}
                  </p>
                ))}
              </div>
            )}
            {dragErrors && (
              <div className="flex flex-col gap-2">
                {dragErrors.map((error) => (
                  <p key={error} className="text-red">
                    {`Error: ${error}`}
                  </p>
                ))}
              </div>
            )}
          </div>
        </div>
      </DragNDrop>
      <div className="flex flex-col gap-4">
        <div
          key="files_list"
          className="flex flex-col justify-between overflow-y-hidden w-[350px]"
          initial={{ opacity: 0, x: '50' }}
          animate={{ opacity: 1, x: '0' }}
          exit={{ opacity: 0, x: '-50' }}
        >
          <Button
            className="text-2xl flex justify-center items-center gap-4"
            disabled={!hasFiles}
            onClick={handleRecordsSpreadsheetImport}
            title={!hasFiles ? 'Files have not yet been selected' : undefined}
          >
            <span>Submit File</span>
            {isUploading && <Spinner size="xs" color={POSITIVE} />}
          </Button>
          <span className="text-red">{uploadError}</span>
          <ul className="mt-2 [&_p]:text-[18px]">
            {[...files].map((file) => (
              <AnimatePresence key={file.name}>
                <motion.li
                  className="flex flex-row items-center my-2"
                  initial={{ opacity: 0, y: 50 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: '-50' }}
                  positionTransition
                >
                  <p className="flex-1 pr-2 whitespace-nowrap overflow-hidden text-ellipsis">{file.name}</p>
                  <CloseButton onClick={() => handleRemoveFile(file)}>
                    <FontAwesomeIcon icon={faTimes} />
                  </CloseButton>
                </motion.li>
              </AnimatePresence>
            ))}
          </ul>
        </div>
      </div>
    </>
  );
};
export const NewPetitionFromRecordSpreadsheet = () => {
  return (
    <div className="flex flex-col gap-10">
      <div className="flex flex-col gap-2">
        <h3>How to Submit the Record Spreadsheet</h3>
        <p>This will allow you to generate petitions from a modified record spreadsheet.</p>
        <p>
          The original record spreadsheet must be downloaded after uploading the PDF record from external record
          provider (CIPRS, Portal, etc.)
        </p>
      </div>
      <RecordUpload />
      <iframe id="printIframe" title="Print" className="h-0 w-0 absolute" />
    </div>
  );
};
