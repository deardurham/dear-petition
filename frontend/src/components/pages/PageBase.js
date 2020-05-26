import React from 'react';
import {
  PageBaseStyled,
  PageHeader,
  PageLogo,
  LogoutButton,
  PageContentWrapper
} from './PageBase.styled';
import DEAR_Logo from '../../assets/img/DEAR_logo.png';

// Ajax
import Axios from '../../service/axios';

// Constants
import { USER } from '../../constants/authConstants';

// Router
import { useHistory } from 'react-router-dom';

function PageBase({ children, ...props }) {
  const history = useHistory();
  const handleLogout = async () => {
    Axios.delete('token/');
    await localStorage.removeItem(USER);
    history.replace('/');
  };

  return (
    <PageBaseStyled {...props}>
      <PageHeader>
        <PageLogo>
          <img src={DEAR_Logo} alt="DEAR logo" />
        </PageLogo>
        <LogoutButton onClick={handleLogout}>Logout</LogoutButton>
      </PageHeader>
      <PageContentWrapper>{children}</PageContentWrapper>
    </PageBaseStyled>
  );
}

export default PageBase;
