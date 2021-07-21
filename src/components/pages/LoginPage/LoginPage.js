import React, { useState } from 'react';
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
import { Redirect, useHistory } from 'react-router-dom';

// AJAX
import Axios from '../../../service/axios';
import { AnimatePresence } from 'framer-motion';
import { USER } from '../../../constants/authConstants';

function Login() {
  const history = useHistory();

  // State
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [errors, setErrors] = useState({});
  const user = localStorage.getItem(USER);

  if (user) {
    return <Redirect to="/" />;
  }

  const handleLogin = async (e) => {
    e.preventDefault();
    setErrors({});
    try {
      const { data, status } = await Axios.post('token/', { username, password });
      if (status === 200 && data.detail === 'success') {
        localStorage.setItem(USER, JSON.stringify(data.user));

        // TODO: remove CSRF token on logout
        history.replace('/');
      }
    } catch (error) {
      if (error.response?.data) {
        setErrors({
          ...errors,
          ...error.response.data,
        });
      }
    }
  };

  return (
    <LoginPageStyled>
      <LoginSplash>
        <SplashLogo src={dearLogo} alt="DEAR logo" />
      </LoginSplash>
      <LoginForm onSubmit={handleLogin}>
        <InputStyled
          label="username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          errors={errors.username}
        />
        <PasswordWrapper>
          <PasswordInputStyled
            label="password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
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
        <Button onClick={handleLogin}>Log in</Button>
      </LoginForm>
    </LoginPageStyled>
  );
}

export default Login;
