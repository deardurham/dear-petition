import React, { useEffect, useRef, useState } from 'react';
import styled from 'styled-components';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faQuestionCircle } from '@fortawesome/free-solid-svg-icons';
import { colorRed } from '../../../styles/colors';
import { fontError } from '../../../styles/fonts';
import {
  HomePageStyled,
  HomeContent,
  DnDContent,
  DragErrors,
  DragWarnings,
} from './HomePage.styled';

import { Tooltip } from '../../elements/Tooltip/Tooltip';
import Modal from '../../elements/Modal/Modal';
import DragNDrop from '../../elements/DragNDrop/DragNDrop';
import FilesList from './FilesList/FilesList';
import { useHistory } from 'react-router-dom';

import { useCreateBatchMutation } from '../../../service/api';

const ALLOWED_MIME_TYPES = ['application/pdf'];
const MAX_FILES = 8;
const MAX_FILE_SIZE = 30000;
const LONG_WAIT_TIMEOUT = 5; // seconds

const ModalStyled = styled(Modal)`
  & > div {
    width: 500px;
    gap: 2rem;
    padding: 4rem;
    p {
      color: ${colorRed};
      font-family: ${fontError};
      font-size: 1.5rem;
      font-weight: bold;
    }
  }
`;

const FilesInputContainer = styled.div`
  display: flex;
  gap: 2rem;
  flex-flow: column;
  align-items: center;
  width: 350px;
`;

const ParserCheckboxWrapper = styled.div`
  align-self: flex-start;
  display: flex;
  align-items: baseline;
  gap: 0.5rem;
  input {
    margin-left: 1rem;
  }
  font-size: 1.75rem;
  color: rgb(68 64 60);
`;

const ExperimentalMessage = styled.div`
  display: flex;
  flex-flow: column;
  gap: 0.5rem;

  padding: 2rem 1.25rem;
  width: 500px;

  p {
    color: rgb(68 64 60);
    font-size: 1.7rem;
  }
`;

function HomePage() {
  const fileInputRef = React.createRef();
  const [parserMode, setParserMode] = useState();
  const [dragWarnings, setDragWarnings] = useState();
  const [dragErrors, setDragErrors] = useState();
  const [files, setFiles] = useState(new Set());
  const [showModal, setShowModal] = useState(false);
  const [modalError, setModalError] = useState();
  const history = useHistory();
  const [createBatch] = useCreateBatchMutation();
  const isMounted = useRef(false);

  useEffect(() => {
    isMounted.current = true;
    return () => {
      isMounted.current = false;
    };
  });

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
    setShowModal(true);
    let timer = null;
    const filesFormData = new FormData();
    files.forEach((file) => filesFormData.append('files', file));
    filesFormData.append('parser_mode', JSON.stringify(parserMode ? 2 : 1));
    timer = setTimeout(() => {
      if (isMounted.current) {
        setModalError(
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
        if (isMounted.current) {
          setModalError('ERROR: Could not process the records.');
        }
      });
  };

  const experimentalParserMessage = (
    <ExperimentalMessage>
      <p>
        Experimental CIPRS Record Reader that can handle records with multi-line offense
        descriptions.
      </p>
      <p>
        Please try this mode if you are having issues with a CIPRS record that has a long offense
        description.
      </p>
    </ExperimentalMessage>
  );

  return (
    <>
      <HomePageStyled>
        <HomeContent>
          <FilesInputContainer>
            <DragNDrop
              ref={fileInputRef}
              mimeTypes={ALLOWED_MIME_TYPES}
              maxFiles={MAX_FILES}
              maxSize={MAX_FILE_SIZE}
              onDrop={handleDrop}
            >
              <DnDContent>
                <div>
                  <h2>Upload CIPRS Records</h2>
                  <p>up to {MAX_FILES} records</p>
                </div>
                <div>
                  {dragWarnings && (
                    <DragWarnings>
                      {dragWarnings.map((warning) => (
                        <p key={warning}>{warning}</p>
                      ))}
                    </DragWarnings>
                  )}
                  {dragErrors && (
                    <DragErrors>
                      {dragErrors.map((error) => (
                        <p key={error}>{error}</p>
                      ))}
                    </DragErrors>
                  )}
                </div>
              </DnDContent>
            </DragNDrop>
            {files && files.size > 0 && (
              <>
                <ParserCheckboxWrapper>
                  (Beta) Multi-Line Reader Mode
                  <Tooltip tooltipContent={experimentalParserMessage}>
                    <FontAwesomeIcon icon={faQuestionCircle} />
                  </Tooltip>
                  <input
                    type="checkbox"
                    checked={!!parserMode}
                    onChange={() => setParserMode((prev) => !prev)}
                  />
                </ParserCheckboxWrapper>
                <FilesList
                  files={files}
                  handleRemoveFile={handleRemoveFile}
                  handlePreparePetitions={handlePreparePetitions}
                />
              </>
            )}
          </FilesInputContainer>
        </HomeContent>
      </HomePageStyled>
      <ModalStyled
        isVisible={showModal}
        closeModal={() => {
          setShowModal(false);
          setModalError();
        }}
      >
        <h2>Preparing petitions...</h2>
        {modalError && <p>{modalError}</p>}
      </ModalStyled>
    </>
  );
}

export default HomePage;
