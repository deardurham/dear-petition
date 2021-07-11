import React, { useEffect, useState } from 'react';
import PropTypes from 'prop-types';
import { DragNDropStyled, FileInputStyled } from './DragNDrop.styled';

const EXCEED_LIMIT_MSG = 'Maximum file limit exceeded';
const BAD_TYPE_MSG = 'One or more of your files is not the right type';

const DragNDrop = React.forwardRef((props, ref) => {
  const { children, mimeTypes, maxFiles, onDrop, onDragEnter, onDragLeave } = props;
  const [draggedOver, setDraggedOver] = useState(false);

  useEffect(() => {
    // If user misses drag target, override browser's default behavior
    function cancel(e) {
      e.preventDefault();
    }
    window.addEventListener('dragover', cancel, false);
    window.addEventListener('drop', cancel, false);
    return () => {
      window.removeEventListener('dragover', cancel, false);
      window.removeEventListener('drop', cancel, false);
    };
  }, []);

  const handleDragEnter = (e) => {
    e.preventDefault();
    setDraggedOver(true);
    if (onDragEnter) onDragEnter(e);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setDraggedOver(false);
    if (onDragLeave) onDragLeave(e);
  };

  const handleDrop = (e) => {
    e.preventDefault();

    const { dropEffect, files } = e.dataTransfer;
    if (dropEffect !== 'none') return;

    _handleFiles(files);
  };

  const handleManualUpload = (e) => {
    _handleFiles(e.target.files);
  };

  const _handleFiles = (files) => {
    const drop = {
      warnings: [],
      errors: [],
      files: [],
    };

    if (files.length > maxFiles) {
      drop.errors.push(EXCEED_LIMIT_MSG);
    } else {
      let badTypes = false;
      for (let i = 0; i < files.length; i++) {
        const file = files[i];
        if (mimeTypes && !mimeTypes.includes(file.type)) {
          badTypes = true;
          continue;
        }

        drop.files.push(file);
      }
      if (badTypes) drop.warnings.push(BAD_TYPE_MSG);
    }

    onDrop(drop);
  };

  return (
    <>
      <FileInputStyled
        ref={ref}
        type="file"
        name="ciprs_file"
        id="ciprs_file"
        onChange={handleManualUpload}
        accept={mimeTypes.join(',')}
        multiple={!maxFiles || maxFiles > 1}
      />
      <DragNDropStyled
        htmlFor="ciprs_file"
        onDragOver={(e) => e.preventDefault()}
        onDragEnter={handleDragEnter}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        draggedOver={draggedOver}
        positionTransition
      >
        {children}
      </DragNDropStyled>
    </>
  );
});

DragNDrop.propTypes = {
  /** Respond to a file drop or input */
  onDrop: PropTypes.func.isRequired,
  mimeTypes: PropTypes.arrayOf(PropTypes.string),
  maxFiles: PropTypes.number,
  onDragEnter: PropTypes.func,
  onDragLeave: PropTypes.func,
};

DragNDrop.defaultProps = {
  mimeTypes: [],
  maxFiles: 8,
  onDragEnter: undefined,
  onDragLeave: undefined,
};

export default DragNDrop;
