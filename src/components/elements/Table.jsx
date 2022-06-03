import React, { useState } from 'react';
import cx from 'classnames';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCaretDown, faCaretUp } from '@fortawesome/free-solid-svg-icons';
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

export const HeaderCell = ({ children, className, tooltip = '' }) => (
  <th className={className} title={tooltip}>
    {children}
  </th>
);

export const TableCell = ({ children, className, header, tooltip }) => {
  if (header) {
    return (
      <th className={className} title={tooltip ?? ''}>
        {children}
      </th>
    );
  }
  return (
    <td className={className} title={tooltip ?? ''}>
      {children}
    </td>
  );
};

export const TableBody = ({ children }) => <tbody>{children}</tbody>;

export const TableHeader = ({ children, sortedHeader, sortDir, onSelectColumn }) => {
  const childrenWithSort = React.Children.map(children, (child) => {
    if (child.type === sortableHeaderType) {
      return (
        <SortableHeader
          key={child.props.field}
          field={child.props.field}
          onSelect={onSelectColumn}
          isSelected={sortedHeader === child.props.field}
          sortDir={sortDir}
        >
          {child.props.children}
        </SortableHeader>
      );
    }
    return child;
  });
  return (
    <thead>
      <tr>{childrenWithSort}</tr>
    </thead>
  );
};

export const TableRow = ({ children, className }) => <tr className={className}>{children}</tr>;

export const Table = ({ children, className, columnSizes, numColumns }) => {
  const defaultSize = `repeat(${numColumns}, 1fr)`;
  return (
    <TableStyle className={className} columnSize={columnSizes || defaultSize}>
      {children}
    </TableStyle>
  );
};

const getOppositeSort = (sortDir) => (sortDir === 'dsc' ? 'asc' : 'dsc');

export const SortableHeader = ({ children, field, onSelect, isSelected, sortDir = 'dsc' }) => {
  const handleClick = () => onSelect(field, isSelected ? getOppositeSort(sortDir) : 'dsc');
  return (
    <HeaderCell>
      <div
        className={cx(
          'flex gap-2 cursor-pointer active:underline-none focus:underline focus:decoration-1 focus:underline-offset-4',
          { 'underline decoration-1 underline-offset-4': isSelected }
        )}
        role="button"
        tabIndex={0}
        onKeyDown={(e) => {
          if (e.key === 'Enter') {
            handleClick();
          }
        }}
        onClick={() => handleClick()}
      >
        {children}
        {isSelected && <FontAwesomeIcon icon={sortDir === 'asc' ? faCaretUp : faCaretDown} />}
      </div>
    </HeaderCell>
  );
};

// handles react hot reloading better: https://stackoverflow.com/a/61846640
const sortableHeaderType = (<SortableHeader />).type;

export const EditableRow = ({ children, isEditing, editingRow }) =>
  isEditing ? <tr>{editingRow}</tr> : <tr>{children}</tr>;
