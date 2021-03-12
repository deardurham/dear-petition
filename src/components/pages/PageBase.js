import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import {
  Link,
  LinksGroup,
  PageBaseStyled,
  PageHeader,
  PageLogo,
  PageContentWrapper
} from './PageBase.styled';
import DEAR_Logo from '../../assets/img/DEAR_logo.png';
import { smallerThanTabletLandscape } from '../../styles/media';

// Ajax
import Axios from '../../service/axios';

// Constants
import { USER, CSRF_TOKEN_LS_KEY } from '../../constants/authConstants';

// Router
import { useHistory } from 'react-router-dom';

const LogoLink = styled(Link)`
  border: none;
  padding: 0;
  height: 80px;
  width: 300px;
  margin: 0;
  @media (${smallerThanTabletLandscape}) {
    width: 400px;
    height: auto;
  }
`;

const LogoutLink = styled(Link)`
  cursor: pointer;
`;

function PageBase({ children, className, ...props }) {
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
      Axios.get('/users/').then(({ data }) => setAdminUrl(data?.results[0].admin_url || ''));
    }
  }, []);

  return (
    <PageBaseStyled {...props}>
      <PageHeader>
          <LogoLink href='/'>
            <PageLogo src={DEAR_Logo} alt="DEAR logo" />
          </LogoLink>
          <LinksGroup>
            {localStorage.getItem(USER) && <Link href='/'>New Petition</Link>}
            {adminUrl ? <Link href={adminUrl}>Admin</Link> : null}
            <LogoutLink onClick={handleLogout}>Logout</LogoutLink>
          </LinksGroup>
      </PageHeader>
      <PageContentWrapper className={className}>{children}</PageContentWrapper>
    </PageBaseStyled>
  );
}

export default PageBase;
