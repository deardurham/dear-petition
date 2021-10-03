import React from 'react';
import { Redirect, Route } from 'react-router-dom';
import PageBase from '../PageBase';
import useAuth from '../../../hooks/useAuth';
import { useUsersQuery } from '../../../service/api';
import { Table, TableBody, TableCell, TableHeader, TableRow } from '../../elements/Table';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCheck, faTimes } from '@fortawesome/free-solid-svg-icons';

const UsersPage = () => {
  const { user: authenticatedUser } = useAuth();
  const { data } = useUsersQuery();
  if (authenticatedUser?.is_admin === false) {
    return <Route render={() => <Redirect to="/" />} />;
  }
  return (
    <PageBase>
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
