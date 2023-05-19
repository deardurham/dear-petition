import { useState } from 'react';
import styled from 'styled-components';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCheck, faTimes } from '@fortawesome/free-solid-svg-icons';
import { useForm } from 'react-hook-form';
import { useModifyUserMutation } from '../../../service/api';
import useAuth from '../../../hooks/useAuth';
import { Button } from '../../elements/Button';
import {
  SortableHeader,
  Table,
  TableBody,
  TableCell,
  TableHeader,
  TableRow,
} from '../../elements/Table';
import Modal from '../../elements/Modal/Modal';
import FormInput from '../../elements/Input/FormInput';

const PassthroughForm = styled.form`
  display: contents;
`;

const PassthroughTD = styled.td`
  display: contents;
`;

const UsersTableStyled = styled(Table)`
  grid-template-columns: minmax(125px, 3fr) minmax(125px, 3fr) minmax(50px, 1fr) minmax(100px, 1fr) minmax(
      50px,
      2fr
    );
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

const TextboxInput = styled(FormInput)`
  width: 100%;
  input {
    width: 100%;
    padding: 0.5rem;
  }
  p {
    white-space: initial;
  }
`;

const formatLastLogin = (lastLogin) => (lastLogin ? new Date(lastLogin).toLocaleDateString() : '');

const DisplayCells = ({ user, onStartEdit }) => {
  const { user: myUser } = useAuth();
  const [isModalVisible, setModalVisible] = useState(false);
  const [triggerUpdate] = useModifyUserMutation();
  const disabledDelete = myUser.pk === user.pk;
  return (
    <>
      <TableCell>{user.username}</TableCell>
      <TableCell>{user.email}</TableCell>
      <TableCell>
        <FontAwesomeIcon icon={user.is_admin ? faCheck : faTimes} />
      </TableCell>
      <TableCell>{formatLastLogin(user.last_login)}</TableCell>
      <TableCell>
        <ActionsRow>
          <ActionButton colorClass="neutral" onClick={() => onStartEdit()}>
            Edit
          </ActionButton>
          <ActionButton
            colorClass={disabledDelete ? 'disabled' : 'caution'}
            disabled={disabledDelete}
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
                colorClass="caution"
                onClick={() => triggerUpdate({ id: user.pk, method: 'delete' })}
              >
                Confirm
              </Button>
              <Button onClick={() => setModalVisible(false)} colorClass="neutral">
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
    control,
    handleSubmit,
    formState: { errors: _formErrors },
    register,
  } = useForm({
    defaultValues: { username: user.username, email: user.email, is_admin: user.is_admin },
  });
  const [triggerUpdate, { error }] = useModifyUserMutation();
  const { user: myUser } = useAuth();
  const onSubmit = async (data) => {
    if (['username', 'email', 'is_admin'].every((field) => user[field] === data[field])) {
      onStopEdit();
    } else {
      try {
        await triggerUpdate({ id: user.pk, data }).unwrap();
        onStopEdit();
      } catch (e) {
        console.error(e);
      }
    }
  };
  return (
    <PassthroughTD>
      <PassthroughForm onSubmit={handleSubmit(onSubmit)}>
        <TableCell>
          <TextboxInput
            inputProps={{ control, name: 'username' }}
            errors={[error?.data?.username] ?? []}
          />
        </TableCell>
        <TableCell>
          <TextboxInput
            inputProps={{ control, name: 'email' }}
            errors={[error?.data?.email] ?? []}
          />
        </TableCell>
        <TableCell>
          <input type="checkbox" disabled={myUser.pk === user.pk} {...register('is_admin')} />
        </TableCell>
        <TableCell>{formatLastLogin(user.last_login)}</TableCell>
        <TableCell>
          <ActionsRow>
            <ActionButton type="submit">Save</ActionButton>
            <ActionButton colorClass="neutral" onClick={() => onStopEdit()}>
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

const UsersTable = ({ ordering, users, setOrdering }) => (
  <UsersTableStyled numColumns={5}>
    <TableHeader>
      <SortableHeader field="username" ordering={ordering} setOrdering={setOrdering}>
        Username
      </SortableHeader>
      <SortableHeader field="email" ordering={ordering} setOrdering={setOrdering}>
        Email
      </SortableHeader>
      <TableCell header>Admin?</TableCell>
      <SortableHeader field="last_login" ordering={ordering} setOrdering={setOrdering}>
        Last Login
      </SortableHeader>
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
