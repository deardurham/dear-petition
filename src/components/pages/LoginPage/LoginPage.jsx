import { useEffect, useState } from 'react';
import { useForm } from 'react-hook-form';
import { useDispatch } from 'react-redux';
import { SplashLogo, FormErrors, InputStyled, PasswordInputStyled } from './LoginPage.styled';
import { Button } from '../../elements/Button';

// Assets
import lancLogoTextless from '../../../assets/img/LANC_logo_textless.png';

// Routing
import { useHistory } from 'react-router-dom';

import { AnimatePresence } from 'framer-motion';
import useAuth from '../../../hooks/useAuth';
import { loggedIn } from '../../../slices/auth';
import { useLoginMutation } from '../../../service/api';
import styled from 'styled-components';

const LoginButton = styled(Button)`
  padding: 1rem 3rem;
  font-size: 1.7rem;
  width: 100%;
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
  }, [authenticatedUser, history]);

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
    <main className="flex-1 flex flex-col gap-12 items-center w-100 h-100 mt-20">
      <div className="max-w-[350px] p-2 flex flex-col items-center">
        <SplashLogo src={lancLogoTextless} alt="DEAR logo" />
        <h1 className="font-sans text-[40px] tracking-wide my-4 text-blue-primary drop-shadow-[0_1.2px_1.2px_rgba(0,0,0,0.3)] font-semibold">
          Easy Expunge
        </h1>
      </div>
      <form className="flex flex-col items-center gap-4 w-[190px]" onSubmit={handleSubmit(handleLogin)}>
        <InputStyled
          className="m-0"
          label="username"
          inputProps={{ name: 'username', control }}
          errors={errors.username}
        />
        <div className="flex flex-col gap-2">
          <PasswordInputStyled
            label="password"
            type="password"
            inputProps={{ name: 'password', control }}
            errors={errors.password}
          />
          <a href="password_reset/">Forgot Password?</a>
        </div>
        <AnimatePresence>
          {errors.detail && (
            <FormErrors
              className="mb-0"
              initial={{ opacity: 0, y: 50 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: '-50' }}
              positionTransition
            >
              <p>{errors.detail}</p>
            </FormErrors>
          )}
        </AnimatePresence>
        <LoginButton type="submit">Log In</LoginButton>
      </form>
    </main>
  );
}

export default Login;
