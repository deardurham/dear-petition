import React from 'react';
import styled from 'styled-components';
import { colorPrimary, greyScale } from '../../styles/colors';

const TableStyle = styled.table`
  display: grid;
  border-collapse: collapse;
  min-width: 100%;
  grid-template-columns: ${(props) => props.columnSize};

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

  & tr:nth-child(even) td {
    background-color: ${greyScale(9.25)};
  }
`;

export const TableCell = ({ children, header }) => (
  <>{header ? <th>{children}</th> : <td>{children}</td>}</>
);

export const TableBody = styled.tbody``;

export const TableHeader = ({ children }) => (
  <thead>
    <tr>{children}</tr>
  </thead>
);

export const TableRow = styled.tr``;

export const Table = ({ children, className, columnSizes, numColumns }) => {
  const defaultSize = `repeat(${numColumns}, 1fr)`;
  return (
    <TableStyle className={className} columnSize={columnSizes || defaultSize}>
      {children}
    </TableStyle>
  );
};
