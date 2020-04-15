import React from 'react';
import { LoginPageStyled, LoginSplash, SplashLogo, LoginSection } from './LoginPage.styled';
import Button from '../../elements/Button/Button';

// Assets
import DEAR_logo from '../../../assets/img/DEAR_logo.png';

// Routing
import { useHistory } from 'react-router-dom';

function Login({ redirect }) {
  const history = useHistory();

  const handleLogin = () => {
    // TODO: Actually log in.
    localStorage.setItem('AUTHORIZED', true);
    history.replace('/')
  }

  return (
    <LoginPageStyled>
      <LoginSplash>
        <SplashLogo src={DEAR_logo} alt='DEAR logo'/>
      </LoginSplash>
      <LoginSection>
        <Button onClick={handleLogin}>Fake log in</Button>
      </LoginSection>
    </LoginPageStyled>
  );
}

export default Login;
