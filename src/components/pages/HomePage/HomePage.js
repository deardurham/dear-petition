import React, { useEffect, useRef, useState } from 'react';
import styled from 'styled-components';
import { colorRed } from '../../../styles/colors';
import { fontError } from '../../../styles/fonts';
import {
  HomePageStyled,
  HomeContent,
  DnDContent,
  DragErrors,
  DragWarnings,
} from './HomePage.styled';

import Modal from '../../elements/Modal/Modal';
import DragNDrop from '../../elements/DragNDrop/DragNDrop';
import FilesList from './FilesList/FilesList';
import { useHistory } from 'react-router-dom';

import { useCreateBatchMutation } from '../../../service/api';

const ALLOWED_MIME_TYPES = ['application/pdf'];
const MAX_FILES = 8;
const MAX_FILE_SIZE = 30000;
const LONG_WAIT_TIMEOUT = 5; // seconds
// TODO: Add timeout to axiosBaseQuery
// const MAX_TIMEOUT = 30; // seconds

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

function HomePage() {
  const fileInputRef = React.createRef();
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

  return (
    <>
      <HomePageStyled>
        <HomeContent>
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
            <FilesList
              files={files}
              handleRemoveFile={handleRemoveFile}
              handlePreparePetitions={handlePreparePetitions}
            />
          )}
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
