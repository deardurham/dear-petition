import React, { useEffect, useState } from 'react';
import { Link, useHistory } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faQuestionCircle, faTimes } from '@fortawesome/free-solid-svg-icons';
import { Button, CloseButton } from '../components/elements/Button';
import DragNDrop from '../components/elements/DragNDrop/DragNDrop';
import { useCreateBatchMutation } from '../service/api';
import { Tooltip } from '../components/elements/Tooltip/Tooltip';

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

export const NewPetition = () => {
  const fileInputRef = React.createRef();
  const [parserMode, setParserMode] = useState(true);
  const [dragWarnings, setDragWarnings] = useState();
  const [dragErrors, setDragErrors] = useState();
  const [uploadError, setUploadError] = useState('');
  const [files, setFiles] = useState(new Set());
  const history = useHistory();
  const [createBatch] = useCreateBatchMutation();
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

  return (
    <div className="flex flex-col">
      <div className="flex flex-col gap-2">
        <p>There are two methods of starting a new expunction petition</p>
        <p>
          1. Email the documents directly from the CIPRS computer.
          <Link to="/help">Click here for instructions</Link>
        </p>
        <p>2. If you have access to the CIPRS record PDF files, you may manually upload them.</p>
      </div>
      <DragNDrop
        className="mt-8 w-[350px] h-[125px]"
        ref={fileInputRef}
        mimeTypes={ALLOWED_MIME_TYPES}
        maxFiles={MAX_FILES}
        maxSize={MAX_FILE_SIZE}
        onDrop={handleDrop}
      >
        <div className="flex flex-col justify-between items-center [&>div]:mt-10">
          <div>
            <h2>Upload CIPRS Files</h2>
            <p className="whitespace-normal">Drag and Drop files here or click to select</p>
          </div>
          <div>
            {dragWarnings && (
              <div className="text-yellow flex flex-col gap-2">
                {dragWarnings.map((warning) => (
                  <p key={warning}>{warning}</p>
                ))}
              </div>
            )}
            {dragErrors && (
              <div className="text-red flex flex-col gap-2">
                {dragErrors.map((error) => (
                  <p key={error}>{error}</p>
                ))}
              </div>
            )}
          </div>
        </div>
      </DragNDrop>
      {files && files.size > 0 && (
        <>
          <div className="flex gap-1 items-baseline self-start">
            (Beta) Multi-Line Reader Mode
            <Tooltip tooltipContent={EXPERIMENTAL_PARSER_MESSAGE}>
              <FontAwesomeIcon icon={faQuestionCircle} />
            </Tooltip>
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
            <Button onClick={handlePreparePetitions}>Prepare petitions</Button>
            {uploadError}
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
        </>
      )}
    </div>
  );
};
