import React, { useState, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faChevronLeft, faChevronRight } from '@fortawesome/free-solid-svg-icons';
import cx from 'classnames';
import styled from 'styled-components';
import UsersTable from './UsersTable';
import PageBase from '../PageBase';
import useDebounce from '../../../hooks/useDebounce';
import { useUsersQuery } from '../../../service/api';
import Select from '../../elements/Input/Select';
import UsersActions from './UsersActions';
import { colorGrey } from '../../../styles/colors';

const UsersSection = styled.div`
  &:not(:last-child) {
    margin-bottom: 2rem;
  }
`;

const UsersHeader = styled.h2`
  margin-bottom: 0.75rem;
`;

const FlexColumn = styled.div`
  display: flex;
  flex-flow: column;
  gap: 15px;
`;

const FlexRow = styled.div`
  display: flex;
  align-items: baseline;
  gap: 15px;
`;

const TableFlexRow = styled(FlexRow)``;

const SearchRow = styled(FlexRow)`
  align-self: center;
  display: flex;
  button {
    padding: 0.75rem;
  }
`;

const SearchBox = styled.input`
  margin-left: 3rem;
  align-self: center;
  width: 20rem;
  padding: 0.9rem;
  border-radius: 3px;
  border: 1px solid ${colorGrey};
`;

const VISIBLE_OFFSET = 2;
const MAX_PAGES = 9;

const limitSizes = [
  { label: '10', value: 10 },
  { label: '25', value: 25 },
  { label: '50', value: 50 },
];

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

const UsersPage = () => {
  const [limit, setLimit] = useState(limitSizes[0]);
  const [offset, setOffset] = useState(0);
  const [ordering, setOrdering] = useState('username');
  const [sortBy, setSortBy] = useState({ field: 'username', dir: 'dsc' });
  const [search, setSearch] = useState('');
  const [formValue, setFormValue] = useState('');
  const debounceSearch = useDebounce((value) => setSearch(value), { timeout: 400 });
  const { data } = useUsersQuery({
    queryString: new URLSearchParams([
      ['search', search],
      ['ordering', ordering],
      ['offset', offset],
      ['limit', limit.value],
    ]).toString(),
  });
  const onSortBy = (field, dir) => {
    setSortBy({ field, dir });
  };

  const numUsers = data?.count ?? 0;
  useEffect(() => {
    if (offset >= numUsers) {
      setOffset(0);
    }
  }, [offset, numUsers]);

  const numPages = Math.floor(numUsers / limit.value) + (numUsers % limit.value > 0 ? 1 : 0);
  const currentPage = offset / limit.value + 1;
  const [startPage, endPage] = calculatePageIndices(currentPage, numPages);
  return (
    <PageBase>
      <UsersSection>
        <UsersHeader>Actions</UsersHeader>
        <UsersActions />
      </UsersSection>
      <UsersSection>
        <UsersHeader>Users</UsersHeader>
        <FlexColumn>
          <TableFlexRow>
            <Select
              label="# of Users to Display"
              value={limit}
              options={limitSizes}
              onChange={(selectObj) => {
                setOffset(0);
                setLimit(selectObj);
              }}
            />
            <SearchRow>
              <SearchBox
                type="text"
                placeholder="Search username or email"
                value={formValue}
                onChange={(e) => {
                  const text = e.target.value;
                  setFormValue(text);
                  debounceSearch(text);
                }}
              />
              {search && (
                <button
                  type="button"
                  className="border border-gray-700 rounded-md"
                  onClick={() => {
                    setFormValue('');
                    setSearch('');
                  }}
                >
                  Clear
                </button>
              )}
            </SearchRow>
            <div className="max-w-[400px] ml-auto self-end flex items-baseline gap-8">
              <button
                type="button"
                onClick={() => setOffset((prev) => prev - limit.value)}
                disabled={!data?.previous}
              >
                <FontAwesomeIcon icon={faChevronLeft} />
              </button>
              <div className="flex items-baseline gap-4">
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
                        'hover:outline hover:text-blue-600 hover:outline-blue-400': !isCurrentPage,
                        'focus:outline focus:text-blue-600 focus:outline-blue-400': !isCurrentPage,
                      })}
                      key={idx}
                      onClick={() => setOffset(idx * limit.value)}
                      disabled={idx === offset / limit.value}
                    >
                      {page}
                    </button>
                  );
                })}
              </div>
              <button
                type="button"
                onClick={() => setOffset((prev) => prev + limit.value)}
                disabled={!data?.next}
              >
                <FontAwesomeIcon icon={faChevronRight} />
              </button>
            </div>
          </TableFlexRow>
          <UsersTable
            users={data?.results || []}
            sortBy={sortBy}
            onSortBy={onSortBy}
            ordering={ordering}
            setOrdering={setOrdering}
          />
        </FlexColumn>
      </UsersSection>
    </PageBase>
  );
};

export default UsersPage;
