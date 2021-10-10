import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPlus } from '@fortawesome/free-solid-svg-icons';
import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import styled from 'styled-components';
import { useCreateUserMutation } from '../../../service/api';
import { Button } from '../../elements/Button';
import Input from '../../elements/Input/Input';

const FlexRow = styled.div`
  display: flex;
  align-items: center;
`;

const ActionFormRow = styled(FlexRow)`
  gap: 15px;
`;

const ButtonContentRow = styled(FlexRow)`
  gap: 10px;
`;

const FlexColumn = styled.div`
  display: flex;
  flex-flow: column;
`;

const SubmitForm = styled.form`
  display: flex;
  gap: 10px;
`;

const USER_ROLES = [
  { label: 'Default User', value: '' },
  { label: 'Administrator', value: 'admin' },
];

/* <Input
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
</SubmitButtonWrapper> */

const CreateUserAction = () => {
  const [isCreating, setIsCreating] = useState(false);
  const [triggerCreateUser, { error }] = useCreateUserMutation();
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();

  const onSubmit = (submitData) => {
    triggerCreateUser({
      username: submitData.username,
      email: submitData.email,
      is_admin: submitData.is_admin === 'admin',
    });
  };

  return (
    <ActionFormRow>
      {!isCreating ? (
        <Button onClick={() => setIsCreating(true)}>
          <ButtonContentRow>
            Create User
            <FontAwesomeIcon icon={faPlus} />
          </ButtonContentRow>
        </Button>
      ) : (
        <SubmitForm onSubmit={handleSubmit(onSubmit)}>
          <input {...register('username')} />
          <input {...register('email')} />
          <select {...register('is_admin')}>
            {Object.values(USER_ROLES).map(({ label, value }) => (
              <option key={value} value={value}>
                {label}
              </option>
            ))}
          </select>
          <Button type="submit">Submit</Button>
          <Button type="neutral" onClick={() => setIsCreating(false)}>
            Cancel
          </Button>
        </SubmitForm>
      )}
    </ActionFormRow>
  );
};

const UsersActions = () => (
  <FlexColumn>
    <CreateUserAction />
  </FlexColumn>
);

export default UsersActions;
