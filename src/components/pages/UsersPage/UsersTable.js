import React, { useState } from 'react';
import styled from 'styled-components';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCheck, faTimes } from '@fortawesome/free-solid-svg-icons';
import { useForm } from 'react-hook-form';
import { useModifyUserMutation } from '../../../service/api';
import useAuth from '../../../hooks/useAuth';
import { Button } from '../../elements/Button';
import { Table, TableBody, TableCell, TableHeader, TableRow } from '../../elements/Table';
import Modal from '../../elements/Modal/Modal';
import Input from '../../elements/Input/Input';

const PassthroughForm = styled.form`
  display: contents;
`;

const PassthroughTD = styled.td`
  display: contents;
`;

const UsersTableStyled = styled(Table)`
  grid-template-columns: minmax(150px, 3fr) minmax(150px, 3fr) minmax(50px, 1fr) minmax(50px, 2fr);
  align-items: center;
  & td {
    height: 100%;
  }
  & form > td {
    display: flex;
    align-items: baseline;
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
  padding: 0.5rem;
`;

const ModalStyled = styled(Modal)`
  & > div {
    width: 450px;
    gap: 1rem;
    & > h2 {
      align-self: center;
    }
    & > p {
      font-size: 1.6rem;
      & > bold {
        font-weight: 600;
      }
    }
    button {
      font-size: 1.6rem;
      padding: 0.5rem;
    }
    & > div:last-child {
      margin-top: 1rem;
      align-self: center;
    }
  }
`;

const TextboxInput = styled(Input)`
  width: 100%;
  input {
    width: 100%;
    padding: 0.5rem;
  }
`;

const DisplayCells = ({ user, onStartEdit }) => {
  const { user: myUser } = useAuth();
  const [isModalVisible, setModalVisible] = useState(false);
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
                setModalVisible(true);
              }
            }}
          >
            Delete
          </ActionButton>
          <ModalStyled isVisible={isModalVisible}>
            <h2>Warning</h2>
            <p>
              Please confirm you want to <bold>permanently</bold> delete the following user:
            </p>
            <p>{user.username}</p>
            <ActionsRow>
              <Button
                type="caution"
                onClick={() => triggerUpdate({ id: user.pk, method: 'delete' })}
              >
                Confirm
              </Button>
              <Button onClick={() => setModalVisible(false)} type="neutral">
                Cancel
              </Button>
            </ActionsRow>
          </ModalStyled>
        </ActionsRow>
      </TableCell>
    </>
  );
};

const InputCells = ({ user, onStopEdit }) => {
  const {
    register,
    handleSubmit,
    formState: { errors: formErrors },
  } = useForm();
  const [triggerUpdate, { error }] = useModifyUserMutation();
  const { user: myUser } = useAuth();
  const onSubmit = (data) => {
    if (myUser.pk === user.pk && user.is_admin !== data.is_admin) {
      console.log('WARNING');
    } else if (!['username', 'email', 'is_admin'].every((field) => user[field] === data[field])) {
      triggerUpdate({ id: user.pk, data })
        .unwrap()
        .then(() => onStopEdit())
        .catch(() => console.error('Validation/network error'));
    } else {
      onStopEdit();
    }
  };
  return (
    <PassthroughTD>
      <PassthroughForm onSubmit={handleSubmit(onSubmit)}>
        <TableCell>
          <TextboxInput
            defaultValue={user.username}
            errors={error?.data?.username ?? ''}
            register={register}
            name="username"
          />
        </TableCell>
        <TableCell>
          <TextboxInput
            defaultValue={user.email}
            errors={error?.data?.email ?? ''}
            register={register}
            name="email"
          />
        </TableCell>
        <TableCell>
          <Input
            type="checkbox"
            defaultChecked={user.is_admin}
            register={register}
            name="is_admin"
          />
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

const UserRow = ({ user, setModalVisible }) => {
  const [isEditing, setEditing] = useState(false);
  return (
    <TableRow key={user.pk}>
      {!isEditing ? (
        <DisplayCells
          user={user}
          onStartEdit={() => setEditing(true)}
          setModalVisible={setModalVisible}
        />
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
