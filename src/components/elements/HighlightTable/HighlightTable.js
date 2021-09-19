import React from 'react';
import styled from 'styled-components';
import { TableBody, TableCell, TableHeader, TableRow, TableStyle } from '../Table';
import { colorPrimary } from '../../../styles/colors';


const StyledTable = ({ children, className, columnSizes, numColumns }) => {
    const defaultSize = `repeat(${numColumns}, 1fr)`;
    return (
      <TableStyle className={className} columnSize={columnSizes || defaultSize}>
        {children}
      </TableStyle>
    );
  };

function HighlightRow({ offenseRecord, highlightRow, unhighlightRow, highlighted, setIsModified }) {

    const handleSelect = () => {
        if (highlighted) {
            unhighlightRow(offenseRecord.pk)
        } else {
            highlightRow(offenseRecord.pk);
        }
        setIsModified(true);
    }

    return (
        <TableRow key={offenseRecord.pk} onClick={() => handleSelect()} highlighted={highlighted}>
            <TableCell><input type="checkbox" checked={highlighted ? true : false} /></TableCell>
            <TableCell>{offenseRecord.dob}</TableCell>
            <TableCell>{offenseRecord.offense_date}</TableCell>
            <TableCell>{offenseRecord.disposition_method}</TableCell>
            <TableCell>{offenseRecord.description}</TableCell>
            <TableCell>{offenseRecord.action}</TableCell>
            <TableCell>{offenseRecord.severity}</TableCell>
            <TableCell>{offenseRecord.law}</TableCell>
        </TableRow>
    )
};

function HighlightTable({ offenseRecords, highlightRow, highlightedRows, unhighlightRow, setIsModified }) {
    return (
        <StyledTable numColumns={8} columnSizes='1fr 4fr 4fr 12fr 8fr 4fr 4fr 6fr'>
            <TableHeader>
                <TableCell header></TableCell>
                <TableCell header>DOB</TableCell>
                <TableCell header>Offense Date</TableCell>
                <TableCell header>Method</TableCell>
                <TableCell header>Description</TableCell>
                <TableCell header>Action</TableCell>
                <TableCell header>Severity</TableCell>
                <TableCell header>Law</TableCell>
            </TableHeader>
            <TableBody>
                {offenseRecords && offenseRecords.map(offenseRecord => (
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
    )
};

export default HighlightTable;
