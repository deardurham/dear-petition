import React, { useState } from 'react';
import { Redirect, Route } from 'react-router-dom';
import PageBase from '../PageBase';
import useAuth from '../../../hooks/useAuth';
import { useCreateUserMutation, useUsersQuery } from '../../../service/api';
import { Table, TableBody, TableCell, TableHeader, TableRow } from '../../elements/Table';
import Input from '../../elements/Input/Input';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCheck, faTimes } from '@fortawesome/free-solid-svg-icons';
import styled from 'styled-components';

const FlexColumn = styled.div`
  display: flex;
  gap: 10px;
`;

const UsersPage = () => {
  const { user: authenticatedUser } = useAuth();
  const [newUsername, setNewUsername] = useState('');
  const [newEmail, setNewEmail] = useState('');
  const [newIsAdmin, setNewIsAdmin] = useState(false);
  const { data } = useUsersQuery();
  const [triggerCreateUser] = useCreateUserMutation();
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
          />
          <Input label="Email" value={newEmail} onChange={(e) => setNewEmail(e.target.value)} />
          <input
            type="checkbox"
            checked={newIsAdmin}
            onChange={() => setNewIsAdmin((prev) => !prev)}
          />
          <div>
            <button
              type="button"
              onClick={() =>
                triggerCreateUser({ username: newUsername, email: newEmail, is_admin: newIsAdmin })
              }
            >
              Submit
            </button>
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
