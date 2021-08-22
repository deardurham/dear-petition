import React from 'react';
import styled from 'styled-components';
import { TableBody, TableCell, TableHeader, TableRow } from '../Table';
import { colorPrimary } from '../../../styles/colors';

const TableStyle = styled.table`
  display: grid;
  border-collapse: collapse;
  min-width: 100%;
  grid-template-columns: ${props => props.columnSize};

  & thead,
  & tbody,
  & tr {
    display: contents;
  }

  & th,
  & td {
    padding: 1rem;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  & th {
    position: sticky;
    top: 0;
    background: ${colorPrimary};
    text-align: left;
    color: white;
    user-select: none;
  }

  & th:last-child {
    border: 0;
  }

  & td {
    padding-top: 10px;
    padding-bottom: 10px;
  }

`;

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
        <StyledTable numColumns={8} columnSizes='.1fr .4fr .4fr 1.2fr .8fr .4fr .4fr .6fr'>
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
