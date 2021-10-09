import React, { useState } from 'react';
import styled from 'styled-components';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCheck, faTimes } from '@fortawesome/free-solid-svg-icons';
import { Button } from '../../elements/Button';
import Input from '../../elements/Input/Input';
import { Table, TableBody, TableCell, TableHeader, TableRow } from '../../elements/Table';

const UsersTableStyled = styled(Table)`
  grid-template-columns: 2fr 2fr 1fr 1fr;
  align-items: center;
  & td {
    height: 100%;
  }
`;

const FlexRow = styled.div`
  display: flex;
  align-items: center;
  height: 100%;
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

const ToggableInputDisplay = ({ children, checked, isInput, label, value, type, onChange }) => {
  if (!isInput) {
    return children || value;
  }
  return (
    <Input
      label={label}
      value={value}
      checked={checked}
      onChange={(e) => onChange(e.target.value)}
      type={type}
    />
  );
};

const UserRow = ({ user }) => {
  const [isEditing, setEditing] = useState(false);
  const [newUsername, setNewUsername] = useState();
  const [newEmail, setNewEmail] = useState();
  const [newRole, setNewRole] = useState(user.is_admin);
  return (
    <TableRow key={user.pk}>
      <TableCell>
        <ToggableInputDisplay
          isInput={isEditing}
          value={newUsername || user.username}
          onChange={(newValue) => setNewUsername(newValue)}
        />
      </TableCell>
      <TableCell>
        <ToggableInputDisplay
          isInput={isEditing}
          value={newEmail || user.email}
          onChange={(newValue) => setNewEmail(newValue)}
        />
      </TableCell>
      <TableCell>
        <FlexRow>
          <ToggableInputDisplay
            isInput={isEditing}
            type="checkbox"
            checked={newRole}
            onChange={() => setNewRole((prev) => !prev)}
          >
            <FontAwesomeIcon icon={user.is_admin ? faCheck : faTimes} />
          </ToggableInputDisplay>
        </FlexRow>
      </TableCell>
      <TableCell>
        <ActionsRow>
          <ActionButton type="neutral" onClick={() => setEditing((prev) => !prev)}>
            {isEditing ? 'Save' : 'Edit'}
          </ActionButton>
          <ActionButton type="caution">Delete</ActionButton>
        </ActionsRow>
      </TableCell>
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
