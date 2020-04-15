import React from 'react';
import { AppStyled } from './App.styled';
import DEARLogo from '../assets/img/DEAR_logo.png';

const App = props => {
  return (
    <AppStyled>
      <img src={DEARLogo} alt='DEAR logo' />
    </AppStyled>
  );
}

export default App;
