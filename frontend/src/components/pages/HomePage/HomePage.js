import React from 'react';
import { HomePageStyled } from './HomePage.styled';
import { useHistory } from 'react-router-dom';
import Button from '../../elements/Button/Button';

function HomePage(props) {
  const history = useHistory();
  return (
    <HomePageStyled>
      <p>HomePage</p>
      <Button onClick={() => history.push('/generate')}>Go to Petition Generation Flow</Button>
    </HomePageStyled>
  );
}

export default HomePage;
