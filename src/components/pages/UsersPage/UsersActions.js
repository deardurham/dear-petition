import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPlus } from '@fortawesome/free-solid-svg-icons';
import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import styled from 'styled-components';
import { useCreateUserMutation } from '../../../service/api';
import { Button } from '../../elements/Button';
import Input from '../../elements/Input/Input';
import Modal from '../../elements/Modal/Modal';

const FlexRow = styled.div`
  display: flex;
  align-items: center;
`;

const ActionFormRow = styled(FlexRow)`
  margin-top: 1rem;
  align-self: center;
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
  flex-flow: column;
  gap: 15px;
  input,
  select,
  button {
    font-size: 1.5rem;
    padding: 0.75rem;
  }
`;

const ModalStyled = styled(Modal)`
  height: 400px;
  width: 450px;
  & > div {
    width: 325px;
    gap: 20px;
    h2 {
      user-select: none;
    }
    input {
      width: 100%;
    }
    span {
      display: block;
      user-select: none;
    }
  }
`;

const USER_ROLES = [
  { label: 'Default User', value: '' },
  { label: 'Administrator', value: 'admin' },
];

const CreateUserAction = ({ onCloseModal }) => {
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
    <>
      <h2>Add User</h2>
      <SubmitForm onSubmit={handleSubmit(onSubmit)}>
        <Input
          label="Username"
          register={register}
          name="username"
          errors={error?.data?.username ?? ''}
        />
        <Input label="Email" register={register} name="email" errors={error?.data?.email ?? ''} />
        <div>
          <span>User Role</span>
          <select {...register('is_admin')}>
            {Object.values(USER_ROLES).map(({ label, value }) => (
              <option key={value} value={value}>
                {label}
              </option>
            ))}
          </select>
        </div>
        <ActionFormRow>
          <div>
            <Button type="submit">Submit</Button>
          </div>
          <div>
            <Button type="neutral" onClick={() => onCloseModal()}>
              Close
            </Button>
          </div>
        </ActionFormRow>
      </SubmitForm>
    </>
  );
};

const UsersActions = () => {
  const [isModalVisible, setModalVisible] = useState(false);
  return (
    <FlexColumn>
      <div>
        <Button onClick={() => setModalVisible(true)}>
          <ButtonContentRow>
            Add User
            <FontAwesomeIcon icon={faPlus} />
          </ButtonContentRow>
        </Button>
      </div>
      <ModalStyled isVisible={isModalVisible}>
        <CreateUserAction onCloseModal={() => setModalVisible(false)} />
      </ModalStyled>
    </FlexColumn>
  );
};

export default UsersActions;
