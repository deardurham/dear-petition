import React from 'react';
import { FilesListWrapper, FilesListStyled, FilesListItem } from './FilesList.styled';
import { AnimatePresence } from 'framer-motion';

// Children
import { Button, CloseButton } from '../../../elements/Button/Button.styled';
import CloseIcon from '../../../elements/Icon/CloseIcon';

function FilesList({ files, handleRemoveFile, handlePreparePetitions, ...props }) {
  return (
    <FilesListWrapper
      {...props}
      key="files_list"
      initial={{ opacity: 0, x: '50' }}
      animate={{ opacity: 1, x: '0' }}
      exit={{ opacity: 0, x: '-50' }}
    >
      <Button onClick={handlePreparePetitions}>Prepare petitions</Button>
      <FilesListStyled>
        {[...files].map((file, i) => {
          return (
            <AnimatePresence key={file.name}>
              <FilesListItem
                initial={{ opacity: 0, y: 50 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: '-50' }}
                positionTransition
              >
                <p>{file.name}</p>
                <CloseButton onClick={() => handleRemoveFile(file)}>
                  <CloseIcon />
                </CloseButton>
              </FilesListItem>
            </AnimatePresence>
          );
        })}
      </FilesListStyled>
    </FilesListWrapper>
  );
}

export default FilesList;
