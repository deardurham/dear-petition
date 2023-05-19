import React, { useEffect, useState } from 'react';
import cx from 'classnames';
import { motion } from 'framer-motion';

const EXCEED_LIMIT_MSG = 'Maximum file limit exceeded';
const BAD_TYPE_MSG = 'One or more of your files is not the right type';

/*
DragNDrop.propTypes = {
  // Respond to a file drop or input
  onDrop: PropTypes.func.isRequired,
  mimeTypes: PropTypes.arrayOf(PropTypes.string),
  maxFiles: PropTypes.number,
  onDragEnter: PropTypes.func,
  onDragLeave: PropTypes.func,
};

DragNDrop.defaultProps = {
  mimeTypes: [],
  maxFiles: 10,
  onDragEnter: undefined,
  onDragLeave: undefined,
};
*/

const DragNDrop = (props, ref) => {
  const { children, className, mimeTypes, maxFiles, onDrop, onDragEnter, onDragLeave } = props;
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

    const { files } = e.dataTransfer;
    if (!files?.length) {
      return;
    }

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
      <input
        ref={ref}
        className="w-[0.1px] h-[0.1px] opacity-0 overflow-hidden absolute -z-10"
        type="file"
        name="ciprs_file"
        id="ciprs_file"
        onChange={handleManualUpload}
        accept={mimeTypes.join(',')}
        multiple={!maxFiles || maxFiles > 1}
      />
      <motion.label
        htmlFor="ciprs_file"
        className={cx(
          className,
          'select-none cursor-pointer min-h-[5px] min-w-[5px] rounded-[2px] border-[5px] border-dashed',
          draggedOver ? 'border-primary' : 'border-gray'
        )}
        onDragOver={(e) => e.preventDefault()}
        onDragEnter={handleDragEnter}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        draggedOver={draggedOver}
        positionTransition
      >
        {children}
      </motion.label>
    </>
  );
};

export default React.forwardRef(DragNDrop);
