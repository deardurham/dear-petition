import React, { useEffect, useState } from 'react';
import { useForm } from 'react-hook-form';
import { useDispatch } from 'react-redux';
import {
  LoginPageStyled,
  LoginSplash,
  SplashLogo,
  LoginForm,
  FormErrors,
  InputStyled,
  PasswordInputStyled,
  ForgotPassword,
  PasswordWrapper,
} from './LoginPage.styled';
import { Button } from '../../elements/Button';

// Assets
import dearLogo from '../../../assets/img/DEAR_logo.png';

// Routing
import { useHistory } from 'react-router-dom';

import { AnimatePresence } from 'framer-motion';
import useAuth from '../../../hooks/useAuth';
import { loggedIn } from '../../../slices/auth';
import { useLoginMutation } from '../../../service/api';
import styled from 'styled-components';

const LoginButton = styled(Button)`
  padding: 1rem 3rem;
`;

function Login() {
  const { user: authenticatedUser } = useAuth();
  const history = useHistory();
  const [login] = useLoginMutation();
  const dispatch = useDispatch();

  // State
  const [errors, setErrors] = useState({});

  useEffect(() => {
    if (authenticatedUser) {
      history.replace('/');
    }
  }, [authenticatedUser]);

  const { control, handleSubmit } = useForm({
    defaultValues: {
      username: '',
      password: '',
    },
  });

  const handleLogin = async ({ username, password }) => {
    // e.preventDefault();
    setErrors({});
    try {
      const { user } = await login({ username, password }).unwrap();
      dispatch(loggedIn(user));
      history.replace('/');
    } catch (error) {
      if (error?.data) {
        setErrors((prev) => ({
          ...prev,
          ...error.data,
        }));
      }
    }
  };

  return (
    <LoginPageStyled>
      <LoginSplash>
        <SplashLogo src={dearLogo} alt="DEAR logo" />
      </LoginSplash>
      <LoginForm onSubmit={handleSubmit(handleLogin)}>
        <InputStyled
          label="username"
          inputProps={{ name: 'username', control }}
          errors={errors.username}
        />
        <PasswordWrapper>
          <PasswordInputStyled
            label="password"
            type="password"
            inputProps={{ name: 'password', control }}
            errors={errors.password}
          />
          <ForgotPassword href="password_reset/">Forgot Password?</ForgotPassword>
        </PasswordWrapper>
        <AnimatePresence>
          {errors.detail && (
            <FormErrors
              initial={{ opacity: 0, y: 50 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: '-50' }}
              positionTransition
            >
              <p>{errors.detail}</p>
            </FormErrors>
          )}
        </AnimatePresence>
        <LoginButton type="submit">Log in</LoginButton>
      </LoginForm>
    </LoginPageStyled>
  );
}

export default Login;
