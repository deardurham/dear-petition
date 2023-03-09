import React, { useEffect, useState } from 'react';
import { useHistory } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faQuestionCircle, faTimes } from '@fortawesome/free-solid-svg-icons';
import { Button, CloseButton } from '../components/elements/Button';
import DragNDrop from '../components/elements/DragNDrop/DragNDrop';
import { useCreateBatchMutation } from '../service/api';
import { Tooltip } from '../components/elements/Tooltip/Tooltip';
import CenteredDialog from '../components/elements/Modal/Dialog';
import { Spinner } from '../components/elements/Spinner';
import { POSITIVE } from '../components/elements/Button/Button';
import useAuth from '../hooks/useAuth';

const ALLOWED_MIME_TYPES = ['application/pdf'];
const MAX_FILES = 10;
const MAX_FILE_SIZE = 30000;
const LONG_WAIT_TIMEOUT = 5; // seconds

const EXPERIMENTAL_PARSER_MESSAGE = (
  <div className="flex flex-col gap-1 p-[2rem_1.25rem] w-[500px]">
    <p>
      Experimental CIPRS Record Reader that can handle records with multi-line offense descriptions.
    </p>
    <p>
      Please try this mode if you are having issues with a CIPRS record that has a long offense
      description.
    </p>
  </div>
);

const RecordUpload = () => {
  const fileInputRef = React.createRef();
  const [parserMode, setParserMode] = useState(true);
  const [dragWarnings, setDragWarnings] = useState();
  const [dragErrors, setDragErrors] = useState();
  const [uploadError, setUploadError] = useState('');
  const [files, setFiles] = useState(new Set());
  const history = useHistory();
  const [createBatch, { isLoading: isUploading }] = useCreateBatchMutation();
  const [isMounted, setIsMounted] = useState(false);

  useEffect(() => {
    setIsMounted(true);
    return () => {
      setIsMounted(false);
    };
  }, []);

  const _mergeFileSets = (newFiles) => {
    const mergedFiles = new Set(files);
    newFiles.forEach((file) => mergedFiles.add(file));
    return mergedFiles;
  };

  const handleDrop = (drop) => {
    setDragErrors(drop.errors);
    setDragWarnings(drop.warnings);
    if (files.size + drop.files.length > MAX_FILES) {
      setDragErrors(['Maximum file limit exceeded']);
      return;
    }

    let hasDups = false;
    files.forEach((file) => {
      const dup = drop.files.find((newFile) => newFile.name === file.name);
      if (dup) {
        setDragErrors([`Cannot upload duplicate file "${dup.name}"`]);
        hasDups = true;
      }
    });
    if (!hasDups) setFiles(_mergeFileSets(drop.files));
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

  const handlePreparePetitions = async () => {
    setUploadError(true);
    let timer = null;
    const filesFormData = new FormData();
    files.forEach((file) => filesFormData.append('files', file));
    filesFormData.append('parser_mode', JSON.stringify(parserMode ? 2 : 1));
    timer = setTimeout(() => {
      if (isMounted) {
        setUploadError(
          'It is taking longer than expected to process the uploaded records. Please wait...'
        );
      }
    }, LONG_WAIT_TIMEOUT * 1000);

    createBatch({ data: filesFormData })
      .unwrap()
      .then((data) => {
        if (timer) {
          clearTimeout(timer);
        }
        history.push(`/generate/${data.id}`);
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
        className="max-w-[350px] min-h-[125px]"
        ref={fileInputRef}
        mimeTypes={ALLOWED_MIME_TYPES}
        maxFiles={MAX_FILES}
        maxSize={MAX_FILE_SIZE}
        onDrop={handleDrop}
      >
        <div className="flex flex-col justify-between items-center gap-4 px-3 py-10">
          <div className="">
            <h2>Upload CIPRS PDF Files</h2>
            <p className="whitespace-normal">
              Drag and Drop files here or click to open file finder
            </p>
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
        <div className="flex gap-4 items-center self-start">
          <span className="flex gap-2">
            (Beta) Multi-Line Reader Mode
            <Tooltip tooltipContent={EXPERIMENTAL_PARSER_MESSAGE}>
              <FontAwesomeIcon icon={faQuestionCircle} />
            </Tooltip>
          </span>
          <input
            type="checkbox"
            checked={!!parserMode}
            onChange={() => setParserMode((prev) => !prev)}
          />
        </div>
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
            onClick={handlePreparePetitions}
            title={!hasFiles ? 'Files have not yet been selected' : undefined}
          >
            <span>Submit Files</span>
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
                  <p className="flex-1 pr-2 whitespace-nowrap overflow-hidden text-ellipsis">
                    {file.name}
                  </p>
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

export const NewPetition = () => {
  const { user } = useAuth();
  const [showEmailModal, setShowEmailModal] = useState(false);
  return (
    <div className="flex flex-col gap-10">
      <div className="flex flex-col gap-2">
        <h3>How to Submit the CIPRS documents</h3>
        <p>There are two methods of starting a new expunction petition</p>
        <p className="flex gap-2">
          1. Email the documents directly from the CIPRS computer.
          <button
            type="button"
            className="text-blue font-semibold"
            onClick={() => setShowEmailModal(true)}
          >
            Click here for instructions
          </button>
        </p>
        <p>2. If you have access to the CIPRS record PDF files, you may manually upload them.</p>
      </div>
      <RecordUpload />
      <iframe id="printIframe" title="Print" className="h-0 w-0 absolute" />
      <CenteredDialog isOpen={showEmailModal} onClose={() => setShowEmailModal(false)}>
        <div id="printableInstructions" className="flex flex-col px-8 py-16 w-[800px]">
          <h3 className="">Upload CIPRS Record via Court Email System</h3>
          <div className="mt-6 [&_li]:text-[17px]">
            <ul className="list-disc list-inside flex flex-col gap-4">
              <li>
                <span>You may send an email with CIPRS record attachments to </span>
                <b>
                  {user.username}
                  @inbox.durhamexpunction.org
                </b>
                <span> to view and generate documents.</span>
              </li>
              <li>
                <span>
                  You may optionally add a label for the CIPRS records by adding a `+`. For example:{' '}
                </span>
                <b>{user.username}+JohnDoeDurhamRecords@inbox.durhamexpunction.org</b>
              </li>
            </ul>
            <div className="mt-6 flex gap-4" media="print" style={{ display: 'none' }}>
              <Button
                onClick={() => {
                  const content = document.getElementById('printableInstructions');
                  const pri = document.getElementById('printIframe').contentWindow;
                  pri.document.open();
                  pri.document.write(content.innerHTML);
                  pri.document.close();
                  pri.focus();
                  pri.print();
                }}
              >
                Print
              </Button>
            </div>
          </div>
        </div>
      </CenteredDialog>
    </div>
  );
};
