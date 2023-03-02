import React from 'react';
import cx from 'classnames';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faCaretDown,
  faCaretUp,
  faChevronLeft,
  faChevronRight,
} from '@fortawesome/free-solid-svg-icons';
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
    overflow: visible;
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

export const calculateNumberOfPages = (count, numPerPage) =>
  Math.floor(count / numPerPage) + (count % numPerPage > 0 ? 1 : 0);

const calculateVisiblePages = (currentPage, numPages, maxVisiblePages = 7) => {
  const offset = 1;
  const lastPageNumber = numPages;
  if (numPages <= maxVisiblePages) {
    return [...Array(numPages).keys()].map((index) => index + 1);
  }
  if (currentPage - offset <= 1) {
    const startingPages = [...Array(maxVisiblePages - 2).keys()].map((index) => index + 1);
    return [...startingPages, lastPageNumber];
  }
  if (currentPage + offset >= lastPageNumber) {
    return [1, ...Array(maxVisiblePages - 2).keys()].map(
      (index) => lastPageNumber - maxVisiblePages + index + 1
    );
  }
  return [1, currentPage - offset, currentPage, currentPage + offset, lastPageNumber];
};

export const PageSelection = ({ currentPage, numPages, onPageSelect }) => {
  const visiblePageNumbers = calculateVisiblePages(currentPage, numPages);
  return (
    <div className="flex-1 flex items-end justify-end gap-4">
      {visiblePageNumbers.map((pageNum, idx) => {
        // gaps in visible pages should be represented as "..."
        const isNotConsecutive = idx > 0 && visiblePageNumbers?.[idx - 1] !== pageNum - 1;
        return (
          <>
            {isNotConsecutive && <span key={idx}>...</span>}
            <button key={idx} type="button" onClick={() => onPageSelect(pageNum)}>
              {pageNum}
            </button>
          </>
        );
      })}
    </div>
  );
};

const VISIBLE_OFFSET = 2;
const MAX_PAGES = 9;
const calculatePageIndices = (current, numPages) => {
  let startIndex = current - VISIBLE_OFFSET;
  let endIndex = current + VISIBLE_OFFSET;
  if (current < MAX_PAGES - 3) {
    startIndex = 1;
    endIndex = Math.max(MAX_PAGES - 2, current + VISIBLE_OFFSET);
  }
  if (current > numPages - MAX_PAGES + 4) {
    startIndex = Math.min(numPages - MAX_PAGES + 3, current - VISIBLE_OFFSET);
    endIndex = numPages;
  }
  return [Math.max(1, startIndex), Math.min(endIndex, numPages)];
};

export const LegacyPageSelection = ({ currentPage, numPages, onPageSelect, disabled }) => {
  const [startPage, endPage] = calculatePageIndices(currentPage, numPages);
  return (
    <div className="flex-1 flex items-end justify-end gap-4">
      <button
        type="button"
        className="disabled:text-gray-400 text-gray-700"
        onClick={() => onPageSelect(currentPage - 1)}
        disabled={currentPage <= 1}
      >
        <FontAwesomeIcon icon={faChevronLeft} />
      </button>
      {[...Array(numPages).keys()].map((idx) => {
        const page = idx + 1;
        const withinLeft = page >= startPage && page <= currentPage;
        const withinRight = page >= currentPage && page <= endPage;
        if (page !== 1 && page !== numPages && !withinLeft && !withinRight) {
          return page === startPage - 1 || page === endPage + 1 ? '...' : null;
        }
        const isCurrentPage = page === currentPage;
        return (
          <button
            type="button"
            className={cx('px-2 py-0.5 outline-1', {
              'outline outline-gray-700': isCurrentPage,
              'hover:outline hover:text-blue-700 hover:outline-blue-400': !isCurrentPage,
              'focus:outline focus:text-blue-700 focus:outline-blue-400': !isCurrentPage,
            })}
            key={idx}
            onClick={() => onPageSelect(page)}
            disabled={disabled}
          >
            {page}
          </button>
        );
      })}
      <button
        type="button"
        className="disabled:text-gray-400 text-gray-700"
        onClick={() => onPageSelect(currentPage + 1)}
        disabled={currentPage >= numPages}
      >
        <FontAwesomeIcon icon={faChevronRight} />
      </button>
    </div>
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
