import { useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faChevronRight,
  faChevronDown,
  faExclamationTriangle,
} from '@fortawesome/free-solid-svg-icons';
import { formatDistance, isBefore, isValid } from 'date-fns';
import {
  TableBody,
  TableCell,
  TableHeader,
  TableRow,
  TableStyle,
} from '../../components/elements/Table';
import { Tooltip } from '../../components/elements/Tooltip/Tooltip';

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

function OffenseRow({ offenseRecord, selected, onSelect, dob }) {
  const [showDetails, setShowDetails] = useState(false);

  const dateAt18YearsOld =
    isValid(dob) && new Date(dob.getFullYear() + 18, dob.getMonth() + dob.getDay());

  return (
    <TableRow key={offenseRecord.pk}>
      <TableCell>
        <input
          type="checkbox"
          className="cursor-pointer"
          checked={!!selected}
          onChange={() => onSelect()}
        />
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
          <Tooltip
            tooltipContent="This offense may be a candidate for the AOC-CR-293 petition form"
            offset={[0, 10]}
          >
            <FontAwesomeIcon className="text-xl text-red-600" icon={faExclamationTriangle} />
          </Tooltip>
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
        <TableCell className="col-span-full">
          <div className="grid grid-cols-[max-content_1fr] gap-2">
            <b>File No:</b>
            {offenseRecord.file_no}
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
        </TableCell>
      )}
    </TableRow>
  );
}

function OffenseTable({ offenseRecords, selectedRows, onSelect, dob }) {
  return (
    <StyledTable
      className="overflow-y-scroll h-[400px] auto-rows-min"
      numColumns={8}
      columnSizes="1fr 3fr 7fr 3fr 3fr 1fr 1fr"
    >
      <TableHeader>
        <TableCell header />
        <TableCell header>Date</TableCell>
        <TableCell header>Description</TableCell>
        <TableCell header>Action</TableCell>
        <TableCell header>Severity</TableCell>
        <TableCell header>
          <FontAwesomeIcon icon={faExclamationTriangle} />
        </TableCell>
        <TableCell header />
      </TableHeader>
      <TableBody>
        {offenseRecords?.map((offenseRecord) => (
          <OffenseRow
            key={offenseRecord.pk}
            selected={selectedRows.includes(offenseRecord.pk)}
            offenseRecord={offenseRecord}
            onSelect={() => onSelect(offenseRecord.pk)}
            dob={dob}
          />
        ))}
      </TableBody>
    </StyledTable>
  );
}

export default OffenseTable;
