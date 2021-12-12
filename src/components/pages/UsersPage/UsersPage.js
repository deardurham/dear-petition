import React, { useState, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faChevronLeft, faChevronRight } from '@fortawesome/free-solid-svg-icons';
import { useHistory } from 'react-router-dom';
import styled from 'styled-components';
import UsersTable from './UsersTable';
import PageBase from '../PageBase';
import useAuth from '../../../hooks/useAuth';
import { useUsersQuery } from '../../../service/api';
import Select from '../../elements/Input/Select';
import UsersActions from './UsersActions';

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

const TableFlexRow = styled(FlexRow)`
  justify-content: space-between;
`;

const PaginationFlexRow = styled(FlexRow)`
  align-self: flex-end;
`;

const limitSizes = [
  { label: '10', value: 10 },
  { label: '25', value: 25 },
  { label: '50', value: 50 },
];

const UsersPage = () => {
  const history = useHistory();
  const { user: authenticatedUser } = useAuth();
  const [limit, setLimit] = useState(limitSizes[0]);
  const [offset, setOffset] = useState(0);
  const { data } = useUsersQuery({ limit: limit.value, offset });

  useEffect(() => {
    if (authenticatedUser?.is_admin !== true) {
      history.replace('/');
    }
  }, [authenticatedUser]);

  const numUsers = data?.count ?? 0;
  useEffect(() => {
    if (offset >= numUsers) {
      setOffset(0);
    }
  }, [offset, numUsers]);

  const numPages = Math.floor(numUsers / limit.value) + (numUsers % limit.value > 0 ? 1 : 0);
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
            <PaginationFlexRow>
              <button
                type="button"
                onClick={() => setOffset((prev) => prev - limit.value)}
                disabled={!data?.previous}
              >
                <FontAwesomeIcon icon={faChevronLeft} />
              </button>
              {[...Array(numPages).keys()].map((idx) => (
                <button
                  type="button"
                  key={idx}
                  onClick={() => setOffset(idx * limit.value)}
                  disabled={idx === offset / limit.value}
                >
                  {idx + 1}
                </button>
              ))}
              <button
                type="button"
                onClick={() => setOffset((prev) => prev + limit.value)}
                disabled={!data?.next}
              >
                <FontAwesomeIcon icon={faChevronRight} />
              </button>
            </PaginationFlexRow>
          </TableFlexRow>
          <UsersTable users={data?.results || []} />
        </FlexColumn>
      </UsersSection>
    </PageBase>
  );
};

export default UsersPage;
