import styled from 'styled-components';
import Input from '../../elements/Input/Input';
import { colorRed } from '../../../styles/colors';
import { motion } from 'framer-motion';

export const LoginPageStyled = styled.main`
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100vw;
`;

export const LoginSplash = styled.div`
  margin-top: calc(10rem + 2vw);
  max-width: 1000px;
  padding: 1rem;
`;

export const SplashLogo = styled.img`
  width: 100%;
  height: auto;
`;

export const LoginForm = styled.form`
  margin-top: 10vh;
  flex: 1;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
`;

export const FormErrors = styled(motion.div)`
  p {
    color: ${colorRed};
  }
`;

export const InputStyled = styled(Input)`
  margin: 2rem 0;
  input {
    padding: 0.9rem;
  }
`;

export const PasswordInputStyled = styled(InputStyled)`
  margin: 0;
`;

export const ForgotPassword = styled.a`
  margin: 0;
`;

export const PasswordWrapper = styled.div`
  margin: 2rem 0;
`;
