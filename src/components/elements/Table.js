import React from 'react';
import styled from 'styled-components';
import { colorPrimary, greyScale } from '../../styles/colors';

const TableStyle = styled.table`
  display: grid;
  border-collapse: collapse;
  min-width: 100%;
  grid-template-columns: ${props => props.columnSize};

  thead, tbody, tr {
    display: contents;
  }

  th, td {
    padding: 1rem;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  th {
    position: sticky;
    top: 0;
    background: ${colorPrimary};
    text-align: left;
    font-weight: bold;
    color: white;
  }

  th:last-child {
    border: 0;
  }
  
  td {
    padding-top: 10px;
    padding-bottom: 10px;
  }
  
  tr:nth-child(even) td {
    background-color: ${greyScale(8)};
  }
`;

export const TableCell = ({ children, header }) => (
  header ? <th>{children}</th> : <td>{children}</td>
);

const TableHeader = ({ children }) => (
  <thead>
    <tr>
      {children}
    </tr>
  </thead>
);

export const TableRow = ({ children }) => (
  <tr>
    {children}
  </tr>
);

export const Table = ({ children, columnSizes, headers, numColumns }) => {
  const size = columnSizes ? `${columnSizes.join(' ')}` : `repeat(${numColumns}, minmax(150px, 1fr))`;
  return (
    <TableStyle columnSize={size}>
      <TableHeader>
        {headers.map((h, i) => <TableCell key={i} header>{h}</TableCell>)}
      </TableHeader>
      <tbody>
        {children}
      </tbody>
    </TableStyle>
  );
}
