import React, { useState } from 'react';
import styled from 'styled-components';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCheck, faTimes } from '@fortawesome/free-solid-svg-icons';
import { useForm } from 'react-hook-form';
import { useModifyUserMutation } from '../../../service/api';
import useAuth from '../../../hooks/useAuth';
import { Button } from '../../elements/Button';
import { Table, TableBody, TableCell, TableHeader, TableRow } from '../../elements/Table';

const PassthroughForm = styled.form`
  display: contents;
`;

const PassthroughTD = styled.td`
  display: contents;
`;

const UsersTableStyled = styled(Table)`
  grid-template-columns: minmax(150px, 2fr) minmax(150px, 2fr) minmax(50px, 1fr) minmax(50px, 1fr);
  align-items: center;
  & td {
    height: 100%;
  }
  & td > input {
    width: 100%;
  }
  & td > * {
    height: 100%;
  }
`;

const ActionsRow = styled.div`
  display: flex;
  align-items: baseline;
  gap: 15px;
  height: 100%;
  gap: 10px;
`;

const ActionButton = styled(Button)`
  padding: 0.25rem;
`;

const DisplayCells = ({ user, onStartEdit }) => {
  const { user: myUser } = useAuth();
  const [triggerUpdate] = useModifyUserMutation();
  return (
    <>
      <TableCell>{user.username}</TableCell>
      <TableCell>{user.email}</TableCell>
      <TableCell>
        <FontAwesomeIcon icon={user.is_admin ? faCheck : faTimes} />
      </TableCell>
      <TableCell>
        <ActionsRow>
          <ActionButton type="neutral" onClick={() => onStartEdit()}>
            Edit
          </ActionButton>
          <ActionButton
            type="caution"
            onClick={() => {
              if (myUser.pk !== user.pk) {
                triggerUpdate({ id: user.pk, method: 'delete' });
              }
            }}
          >
            Delete
          </ActionButton>
        </ActionsRow>
      </TableCell>
    </>
  );
};

const InputCells = ({ user, onStopEdit }) => {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();
  const [triggerUpdate] = useModifyUserMutation();
  const { user: myUser } = useAuth();
  const onSubmit = (data) => {
    if (myUser.pk === user.pk && user.is_admin !== data.is_admin) {
      console.log('WARNING');
    } else if (!['username', 'email', 'is_admin'].every((field) => user[field] === data[field])) {
      triggerUpdate({ id: user.pk, data });
    }
    onStopEdit();
  };
  return (
    <PassthroughTD>
      <PassthroughForm onSubmit={handleSubmit(onSubmit)}>
        <TableCell>
          <input defaultValue={user.username} {...register('username')} />
        </TableCell>
        <TableCell>
          <input defaultValue={user.email} {...register('email')} />
        </TableCell>
        <TableCell>
          <div>
            <input type="checkbox" defaultChecked={user.is_admin} {...register('is_admin')} />
          </div>
        </TableCell>
        <TableCell>
          <ActionsRow>
            <ActionButton type="submit">Save</ActionButton>
            <ActionButton type="neutral" onClick={() => onStopEdit()}>
              Cancel
            </ActionButton>
          </ActionsRow>
        </TableCell>
      </PassthroughForm>
    </PassthroughTD>
  );
};

const UserRow = ({ user }) => {
  const [isEditing, setEditing] = useState(false);
  return (
    <TableRow key={user.pk}>
      {!isEditing ? (
        <DisplayCells user={user} onStartEdit={() => setEditing(true)} />
      ) : (
        <InputCells user={user} onStopEdit={() => setEditing(false)} />
      )}
    </TableRow>
  );
};

const UsersTable = ({ users }) => (
  <UsersTableStyled numColumns={4}>
    <TableHeader>
      <TableCell header>Username</TableCell>
      <TableCell header>Email</TableCell>
      <TableCell header>Admin?</TableCell>
      <TableCell header>Actions</TableCell>
    </TableHeader>
    <TableBody>
      {users.map((user) => (
        <UserRow key={user.pk} user={user} />
      ))}
    </TableBody>
  </UsersTableStyled>
);

export default UsersTable;
