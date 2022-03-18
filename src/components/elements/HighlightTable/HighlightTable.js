import React, { useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faChevronRight,
  faChevronDown,
  faExclamationCircle,
  faFlag,
} from '@fortawesome/free-solid-svg-icons';
import { formatDistance, isBefore, isValid } from 'date-fns';
import { TableBody, TableCell, TableHeader, TableRow, TableSpanCell, TableStyle } from '../Table';

function StyledTable({ children, className, columnSizes, numColumns }) {
  const defaultSize = `repeat(${numColumns}, 1fr)`;
  return (
    <TableStyle className={className} columnSize={columnSizes || defaultSize}>
      {children}
    </TableStyle>
  );
}

const toNormalCaseEachWord = (str) =>
  str
    .split(' ')
    .map(toNormalCase)
    .reduce((acc, s) => `${acc} ${s}`);
const toNormalCase = (str) => `${str.charAt(0).toUpperCase()}${str.slice(1).toLowerCase()}`;

function HighlightRow({
  offenseRecord,
  highlightRow,
  unhighlightRow,
  highlighted,
  setIsModified,
  dob,
}) {
  const [showDetails, setShowDetails] = useState(false);
  const handleSelect = () => {
    if (highlighted) {
      unhighlightRow(offenseRecord.pk);
    } else {
      highlightRow(offenseRecord.pk);
    }
    setIsModified(true);
  };

  const dateAt18YearsOld =
    isValid(dob) && new Date(dob.getFullYear() + 18, dob.getMonth() + dob.getDay());

  return (
    <TableRow key={offenseRecord.pk} highlighted={highlighted}>
      <TableCell>
        <input type="checkbox" checked={!!highlighted} onChange={() => handleSelect()} />
      </TableCell>
      <TableCell tooltip={offenseRecord.offense_date}>{offenseRecord.offense_date}</TableCell>
      <TableCell tooltip={offenseRecord.description}>{offenseRecord.description}</TableCell>
      <TableCell tooltip={offenseRecord.action}>
        {toNormalCaseEachWord(offenseRecord.action)}
      </TableCell>
      <TableCell tooltip={offenseRecord.severity}>
        {toNormalCaseEachWord(offenseRecord.severity)}
      </TableCell>
      <TableCell>
        {isValid(dob) && isBefore(new Date(offenseRecord.offense_date), dateAt18YearsOld) && (
          <FontAwesomeIcon className="text-3xl text-red-600" icon={faExclamationCircle} />
        )}
      </TableCell>
      <TableCell>
        <button type="button" onClick={() => setShowDetails((prev) => !prev)}>
          {showDetails ? (
            <FontAwesomeIcon icon={faChevronDown} />
          ) : (
            <FontAwesomeIcon icon={faChevronRight} />
          )}
        </button>
      </TableCell>
      {showDetails && (
        <TableSpanCell className="col-span-7">
          <div className="grid grid-cols-[max-content_1fr] gap-2">
            {isValid(dob) && offenseRecord?.offense_date && (
              <>
                <b>Estimated Age:</b>
                {formatDistance(dob, new Date(offenseRecord.offense_date))}
              </>
            )}
            <b>Method:</b>
            {offenseRecord.disposition_method}
            <b>Law:</b>
            {offenseRecord.law}
          </div>
        </TableSpanCell>
      )}
    </TableRow>
  );
}

function HighlightTable({
  offenseRecords,
  highlightRow,
  highlightedRows,
  unhighlightRow,
  setIsModified,
  dob,
}) {
  return (
    <StyledTable
      className="overflow-auto max-h-[500px] auto-rows-min"
      numColumns={8}
      columnSizes="1fr 3fr 7fr 4fr 4fr 2fr 1fr"
    >
      <TableHeader>
        <TableCell header />
        <TableCell header>Offense Date</TableCell>
        <TableCell header>Description</TableCell>
        <TableCell header>Action</TableCell>
        <TableCell header>Severity</TableCell>
        <TableCell header>
          <FontAwesomeIcon icon={faFlag} />
        </TableCell>
        <TableCell header />
      </TableHeader>
      <TableBody>
        {offenseRecords &&
          offenseRecords.map((offenseRecord) => (
            <HighlightRow
              key={offenseRecord.pk}
              offenseRecord={offenseRecord}
              highlightRow={highlightRow}
              unhighlightRow={unhighlightRow}
              highlighted={highlightedRows.includes(offenseRecord.pk)}
              setIsModified={setIsModified}
              dob={dob}
            />
          ))}
      </TableBody>
    </StyledTable>
  );
}

export default HighlightTable;
