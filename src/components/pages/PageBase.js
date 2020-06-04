import React, { useState, useEffect } from 'react';
import {
  PageBaseStyled,
  PageHeader,
  PageLogo,
  AdminButton,
  LogoutButton,
  PageContentWrapper
} from './PageBase.styled';
import DEAR_Logo from '../../assets/img/DEAR_logo.png';

// Ajax
import Axios from '../../service/axios';

// Constants
import { USER, CSRF_TOKEN_LS_KEY } from '../../constants/authConstants';

// Router
import { useHistory } from 'react-router-dom';

function PageBase({ children, ...props }) {
  const [adminUrl, setAdminUrl] = useState('');
  const history = useHistory();
  const handleLogout = () => {
    Axios.delete('token/');
    localStorage.removeItem(CSRF_TOKEN_LS_KEY);
    localStorage.removeItem(USER);
    history.replace('/');
  };

  useEffect(() => {
    if (localStorage.getItem(USER)) {
      Axios.get('/users/').then((data) => setAdminUrl(data.admin_url));
    }
  }, []);

  return (
    <PageBaseStyled {...props}>
      <PageHeader>
        <PageLogo>
          <img src={DEAR_Logo} alt="DEAR logo" />
        </PageLogo>
        {adminUrl ? <AdminButton href={adminUrl}>Admin</AdminButton> : null}
        <LogoutButton onClick={handleLogout}>Logout</LogoutButton>
      </PageHeader>
      <PageContentWrapper>{children}</PageContentWrapper>
    </PageBaseStyled>
  );
}

export default PageBase;
