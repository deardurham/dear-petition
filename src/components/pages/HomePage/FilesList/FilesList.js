import React from 'react';
import { FilesListWrapper, FilesListStyled, FilesListItem } from './FilesList.styled';
import { AnimatePresence } from 'framer-motion';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTimes } from '@fortawesome/free-solid-svg-icons';

// Children
import { Button, CloseButton } from '../../../elements/Button';
import styled from 'styled-components';

const PrepareButton = styled(Button)`
  font-size: 20px;
  padding: 0.5rem;
`;

function FilesList({ files, handleRemoveFile, handlePreparePetitions, ...props }) {
  return (
    <FilesListWrapper
      {...props}
      key="files_list"
      initial={{ opacity: 0, x: '50' }}
      animate={{ opacity: 1, x: '0' }}
      exit={{ opacity: 0, x: '-50' }}
    >
      <PrepareButton onClick={handlePreparePetitions}>Prepare petitions</PrepareButton>
      <FilesListStyled>
        {[...files].map((file) => (
          <AnimatePresence key={file.name}>
            <FilesListItem
              initial={{ opacity: 0, y: 50 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: '-50' }}
              positionTransition
            >
              <p>{file.name}</p>
              <CloseButton onClick={() => handleRemoveFile(file)}>
                <FontAwesomeIcon icon={faTimes} />
              </CloseButton>
            </FilesListItem>
          </AnimatePresence>
        ))}
      </FilesListStyled>
    </FilesListWrapper>
  );
}

export default FilesList;
