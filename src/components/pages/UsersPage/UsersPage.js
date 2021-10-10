import React, { useState, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faChevronLeft, faChevronRight } from '@fortawesome/free-solid-svg-icons';
import { useForm } from 'react-hook-form';
import { useHistory } from 'react-router-dom';
import styled from 'styled-components';
import UsersTable from './UsersTable';
import PageBase from '../PageBase';
import useAuth from '../../../hooks/useAuth';
import { useCreateUserMutation, useUsersQuery } from '../../../service/api';
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
  align-items: baseline;
  gap: 15px;
`;

const TableFlexRow = styled(FlexRow)`
  justify-content: space-between;
`;

const PaginationFlexRow = styled(FlexRow)`
  align-self: flex-end;
`;

const SubmitButtonWrapper = styled.div`
  align-self: center;
  & > button {
    padding: 0.75rem;
    font-weight: 600;
  }
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
  const history = useHistory();
  const { user: authenticatedUser } = useAuth();
  const [limit, setLimit] = useState(limitSizes[0]);
  const [offset, setOffset] = useState(0);
  const { data } = useUsersQuery({ limit: limit.value, offset });
  const [triggerCreateUser, { error }] = useCreateUserMutation();
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();

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

  const onSubmit = (submitData) => {
    console.log(submitData);
    triggerCreateUser({
      username: submitData.username,
      email: submitData.email,
      is_admin: submitData.is_admin === 'admin',
    });
  };

  const numPages = Math.floor(numUsers / limit.value) + (numUsers % limit.value > 0 ? 1 : 0);
  return (
    <PageBase>
      <div>
        <h2>Actions</h2>
        <FlexRow>
          <form onSubmit={handleSubmit(onSubmit)}>
            <input {...register('username')} />
            <input {...register('email')} />
            <select {...register('is_admin')}>
              {Object.values(userRoles).map(({ label, value }) => (
                <option key={value} value={value}>
                  {label}
                </option>
              ))}
            </select>
            <Button type="submit">Create User</Button>
          </form>
          {/* <Input
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
          <SubmitButtonWrapper>
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
          </SubmitButtonWrapper> */}
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
    </PageBase>
  );
};

export default UsersPage;
