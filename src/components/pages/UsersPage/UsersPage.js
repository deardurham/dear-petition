import React, { useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCheck, faChevronLeft, faChevronRight, faTimes } from '@fortawesome/free-solid-svg-icons';
import { Redirect, Route } from 'react-router-dom';
import styled from 'styled-components';
import PageBase from '../PageBase';
import useAuth from '../../../hooks/useAuth';
import { useCreateUserMutation, useUsersQuery } from '../../../service/api';
import { Table, TableBody, TableCell, TableHeader, TableRow } from '../../elements/Table';
import { Button } from '../../elements/Button';
import Input from '../../elements/Input/Input';
import Select from '../../elements/Input/Select';

const FlexColumn = styled.div`
  display: flex;
  flex-flow: column;
  gap: 15px;
`;

const FlexRow = styled.div`
  display: flex;
  align-items: center;
  gap: 15px;
`;

const TableFlexRow = styled(FlexRow)`
  justify-content: space-between;
`;

const UsersTable = styled(Table)`
  grid-template-columns: 1fr 3fr 3fr 2fr 3fr;
`;

const ActionsRow = styled(FlexRow)`
  height: 100%;
  gap: 10px;
`;

const ActionButton = styled(Button)`
  padding: 0.25rem;
`;

const SubmitButton = styled(Button)`
  padding: 0.75rem;
  font-weight: 600;
`;

const userRoles = [
  { label: 'Default User', value: '' },
  { label: 'Administrator', value: 'admin' },
];

const limitSizes = [
  { label: '10', value: 10 },
  { label: '25', value: 25 },
  { label: '50', value: 50 },
];

const UsersPage = () => {
  const { user: authenticatedUser } = useAuth();
  const [newUsername, setNewUsername] = useState('');
  const [newEmail, setNewEmail] = useState('');
  const [newRole, setNewRole] = useState(userRoles[0]);
  const [limit, setLimit] = useState(limitSizes[0]);
  const [offset, setOffset] = useState(0);
  const { data } = useUsersQuery({ limit: limit.value, offset });
  const [triggerCreateUser, { error }] = useCreateUserMutation();
  if (authenticatedUser?.is_admin === false) {
    return <Route render={() => <Redirect to="/" />} />;
  }
  return (
    <PageBase>
      <div>
        <h2>Actions</h2>
        <FlexRow>
          <Input
            label="Username"
            value={newUsername}
            onChange={(e) => setNewUsername(e.target.value)}
            errors={error?.data?.username ?? ''}
          />
          <Input
            label="Email"
            value={newEmail}
            onChange={(e) => setNewEmail(e.target.value)}
            errors={error?.data?.email ?? ''}
          />
          <Select
            label="User Role"
            value={newRole}
            onChange={(selectObj) => setNewRole(selectObj)}
            options={userRoles}
          />
          <div>
            <SubmitButton
              onClick={() =>
                triggerCreateUser({
                  username: newUsername,
                  email: newEmail,
                  is_admin: newRole.value === 'admin',
                })
              }
            >
              Submit
            </SubmitButton>
          </div>
        </FlexRow>
      </div>
      <h2>Users</h2>
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
          <TableFlexRow>
            <button
              type="button"
              onClick={() => setOffset((prev) => prev - limit.value)}
              disabled={!data?.previous}
            >
              <FontAwesomeIcon icon={faChevronLeft} />
            </button>
            {[...Array(Math.floor(+(data?.count ?? 0) / limit.value) + 1).keys()].map((idx) => (
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
          </TableFlexRow>
        </TableFlexRow>
        <UsersTable numColumns={5}>
          <TableHeader>
            <TableCell header />
            <TableCell header>Username</TableCell>
            <TableCell header>Email</TableCell>
            <TableCell header>Admin?</TableCell>
            <TableCell header>Actions</TableCell>
          </TableHeader>
          <TableBody>
            {data?.results &&
              data.results.map((user) => (
                <TableRow key={user.pk}>
                  <TableCell>
                    <Input type="checkbox" />
                  </TableCell>
                  <TableCell>{user.username}</TableCell>
                  <TableCell>{user.email}</TableCell>
                  <TableCell>
                    <FontAwesomeIcon icon={user.is_admin ? faCheck : faTimes} />
                  </TableCell>
                  <TableCell>
                    <ActionsRow>
                      <ActionButton type="neutral">Edit</ActionButton>
                      <ActionButton type="caution">Delete</ActionButton>
                    </ActionsRow>
                  </TableCell>
                </TableRow>
              ))}
          </TableBody>
        </UsersTable>
      </FlexColumn>
    </PageBase>
  );
};

export default UsersPage;
