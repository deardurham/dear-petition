import React, { useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCheck, faTimes } from '@fortawesome/free-solid-svg-icons';
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
  align-items: center;
  gap: 15px;
`;

const userRoles = [
  { label: 'Default User', value: '' },
  { label: 'Administrator', value: 'admin' },
];

const UsersPage = () => {
  const { user: authenticatedUser } = useAuth();
  const [newUsername, setNewUsername] = useState('');
  const [newEmail, setNewEmail] = useState('');
  const [newRole, setNewRole] = useState(userRoles[0]);
  const { data } = useUsersQuery();
  const [triggerCreateUser, { error }] = useCreateUserMutation();
  if (authenticatedUser?.is_admin === false) {
    return <Route render={() => <Redirect to="/" />} />;
  }
  return (
    <PageBase>
      <div>
        <h1>Actions</h1>
        <FlexColumn>
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
            <Button
              onClick={() =>
                triggerCreateUser({
                  username: newUsername,
                  email: newEmail,
                  is_admin: newRole.value === 'admin',
                })
              }
            >
              Submit
            </Button>
          </div>
        </FlexColumn>
      </div>
      <h1>Users</h1>
      <Table numColumns={3}>
        <TableHeader>
          <TableCell header>Username</TableCell>
          <TableCell header>Email</TableCell>
          <TableCell header>Admin?</TableCell>
        </TableHeader>
        <TableBody>
          {data?.results &&
            data.results.map((user) => (
              <TableRow key={user.pk}>
                <TableCell>{user.username}</TableCell>
                <TableCell>{user.email}</TableCell>
                <TableCell>
                  <FontAwesomeIcon icon={user.is_admin ? faCheck : faTimes} />
                </TableCell>
              </TableRow>
            ))}
        </TableBody>
      </Table>
    </PageBase>
  );
};

export default UsersPage;
