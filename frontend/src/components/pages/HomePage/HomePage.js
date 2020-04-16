import React, { useState } from 'react';
import {
  HomePageStyled,
  HomeContent,
  DnDContent,
  DragErrors,
  DragWarnings,
} from './HomePage.styled';

// Children
import DragNDrop from '../../elements/DragNDrop/DragNDrop';
import FilesList from './FilesList/FilesList';

const MAX_FILES = 8;
const MAX_FILE_SIZE = 30_000;

function HomePage(props) {
  const [dragWarnings, setDragWarnings] = useState();
  const [dragErrors, setDragErrors] = useState();
  const [files, setFiles] = useState([]);

  const handleDrop = (drop) => {
    setDragErrors(drop.errors);
    setDragWarnings(drop.warnings);
    if (files.length + drop.files.length > MAX_FILES) {
      setDragErrors(['Maximum file limit exceeded']);
      return;
    }
    // TODO: Reject files with duplicate file.name
    setFiles([...files, ...drop.files]);
  };

  const handleRemoveFile = (rmFile) => {
    setFiles(files.filter((fl) => fl.name !== rmFile.name));
  };

  const handleGeneratePetition = () => {
    console.log('pretending to generate petition!');
  };

  return (
    <HomePageStyled>
      <HomeContent>
        {files.length > 0 && (
          <FilesList
            files={files}
            handleRemoveFile={handleRemoveFile}
            handleGeneratePetition={handleGeneratePetition}
          />
        )}
        <DragNDrop
          mimeTypes={['application/pdf']}
          maxFiles={MAX_FILES}
          maxSize={MAX_FILE_SIZE}
          onDrop={handleDrop}
        >
          <DnDContent>
            <div>
              <h2>Upload CIPRS Records</h2>
              <p>up to 5 records</p>
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
      </HomeContent>
    </HomePageStyled>
  );
}

export default HomePage;
