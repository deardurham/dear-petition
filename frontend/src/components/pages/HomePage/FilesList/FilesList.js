import React from 'react';
import { FilesListWrapper, FilesListStyled, FilesListItem } from './FilesList.styled';
import Button from '../../../elements/Button/Button';

function FilesList({ files = [], handleRemoveFile, handleGeneratePetition }) {
  return (
    <FilesListWrapper>
      <FilesListStyled>
        {files.map(file => {
          return (
            <FilesListItem key={file.name}>
              <p>{file.name}</p>
              <span onClick={() => handleRemoveFile(file)}>x</span>
            </FilesListItem>
          );
        })}
      </FilesListStyled>
      <Button onClick={handleGeneratePetition}>Create petition</Button>
    </FilesListWrapper>
  );
}

export default FilesList;
