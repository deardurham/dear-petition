import React from 'react';
import styled from 'styled-components';
import { colorPrimary, greyScale } from '../../styles/colors';

export const TableStyle = styled.table`
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

export const TableSpanCell = styled.td`
  grid-column: 1 / span ${(props) => props.spanLength};
`;

export const TableBody = ({ children }) => <tbody>{children}</tbody>;

export const TableHeader = ({ children }) => (
  <thead>
    <tr>{children}</tr>
  </thead>
);

export const TableRow = styled.tr`
  & > td {
    ${(props) =>
      props.highlighted
        ? `
  background-color: rgb(255, 245, 217);
  `
        : `background-color: ${props.backgroundColor}`}
  }
  cursor: pointer;

  input[type='checkbox'] {
    cursor: pointer;
  }
`;

export const Table = ({ children, className, columnSizes, numColumns }) => {
  const defaultSize = `repeat(${numColumns}, 1fr)`;
  return (
    <TableStyle className={className} columnSize={columnSizes || defaultSize}>
      {children}
    </TableStyle>
  );
};
