import React from 'react';
import { TableBody, TableCell, TableHeader, TableRow, TableStyle } from '../Table';

function StyledTable({ children, className, columnSizes, numColumns }) {
  const defaultSize = `repeat(${numColumns}, 1fr)`;
  return (
    <TableStyle className={className} columnSize={columnSizes || defaultSize}>
      {children}
    </TableStyle>
  );
}

function HighlightRow({ offenseRecord, highlightRow, unhighlightRow, highlighted, setIsModified }) {
  const handleSelect = () => {
    if (highlighted) {
      unhighlightRow(offenseRecord.pk);
    } else {
      highlightRow(offenseRecord.pk);
    }
    setIsModified(true);
  };

  return (
    <TableRow key={offenseRecord.pk} highlighted={highlighted}>
      <TableCell>
        <input type="checkbox" checked={!!highlighted} onChange={() => handleSelect()} />
      </TableCell>
      <TableCell tooltip={offenseRecord.dob}>{offenseRecord.dob}</TableCell>
      <TableCell tooltip={offenseRecord.offense_date}>{offenseRecord.offense_date}</TableCell>
      <TableCell tooltip={offenseRecord.disposition_method}>
        {offenseRecord.disposition_method}
      </TableCell>
      <TableCell tooltip={offenseRecord.description}>{offenseRecord.description}</TableCell>
      <TableCell tooltip={offenseRecord.action}>{offenseRecord.action}</TableCell>
      <TableCell tooltip={offenseRecord.severity}>{offenseRecord.severity}</TableCell>
      <TableCell tooltip={offenseRecord.law}>{offenseRecord.law}</TableCell>
    </TableRow>
  );
}

function HighlightTable({
  offenseRecords,
  highlightRow,
  highlightedRows,
  unhighlightRow,
  setIsModified,
}) {
  return (
    <StyledTable numColumns={8} columnSizes="1fr 4fr 4fr 12fr 8fr 4fr 4fr 6fr">
      <TableHeader>
        <TableCell header />
        <TableCell header>DOB</TableCell>
        <TableCell header>Offense Date</TableCell>
        <TableCell header>Method</TableCell>
        <TableCell header>Description</TableCell>
        <TableCell header>Action</TableCell>
        <TableCell header>Severity</TableCell>
        <TableCell header>Law</TableCell>
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
            />
          ))}
      </TableBody>
    </StyledTable>
  );
}

export default HighlightTable;
