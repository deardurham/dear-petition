import React from 'react';
import { FilesListWrapper, FilesListStyled, FilesListItem } from './FilesList.styled';
import { AnimatePresence } from 'framer-motion';

// Children
import Button from '../../../elements/Button/Button';

function FilesList({ files, handleRemoveFile, handlePreparePetitions, ...props }) {
  return (
    <FilesListWrapper
      {...props}
      key="files_list"
      initial={{ opacity: 0, x: '50' }}
      animate={{ opacity: 1, x: '0' }}
      exit={{ opacity: 0, x: '-50' }}
    >
      <FilesListStyled>
        {[...files].map((file, i) => {
          return (
            <AnimatePresence key={file.name}>
              <FilesListItem
                initial={{ opacity: 0, x: 50 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: '-50' }}
                positionTransition
              >
                <p>{file.name}</p>
                <span onClick={() => handleRemoveFile(file)}>x</span>
              </FilesListItem>
            </AnimatePresence>
          );
        })}
      </FilesListStyled>
      <Button onClick={handlePreparePetitions}>Prepare petitions</Button>
    </FilesListWrapper>
  );
}

export default FilesList;
