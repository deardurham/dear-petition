import React from 'react';
import { useDispatch } from 'react-redux';
import { Link, useHistory } from 'react-router-dom';
import styled from 'styled-components';
import {
  LinkWrapper,
  LinksGroup,
  PageBaseStyled,
  PageHeader,
  PageLogo,
  PageContentWrapper,
} from './PageBase.styled';
import dearLogo from '../../assets/img/DEAR_logo.png';
import { smallerThanTabletLandscape } from '../../styles/media';

import useAuth from '../../hooks/useAuth';
import { useLogoutMutation } from '../../service/api';
import { loggedOut } from '../../slices/auth';

const LogoLink = styled(LinkWrapper)`
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

const LogoutLink = styled(LinkWrapper)`
  cursor: pointer;
`;

function PageBase({ children, className, ...props }) {
  const history = useHistory();
  const { user } = useAuth();
  const dispatch = useDispatch();
  const [logout] = useLogoutMutation();

  return (
    <PageBaseStyled {...props}>
      <PageHeader>
        <LogoLink>
          <Link to="/">
            <PageLogo src={dearLogo} alt="DEAR logo" />
          </Link>
        </LogoLink>
        <LinksGroup>
          {user && (
            <LinkWrapper>
              <Link to="/">New Petition</Link>
            </LinkWrapper>
          )}
          <LinkWrapper>
            <Link to="/help">Help</Link>
          </LinkWrapper>
          {user?.is_admin ? (
            <LinkWrapper>
              <Link to="/users">Users</Link>
            </LinkWrapper>
          ) : null}
          {user?.is_admin ? (
            <LinkWrapper>
              <a href={user.admin_url}>Admin</a>
            </LinkWrapper>
          ) : null}
          <LogoutLink
            to="/"
            onClick={() =>
              logout().then(() => {
                dispatch(loggedOut());
                history.replace('/login');
              })
            }
          >
            Logout
          </LogoutLink>
        </LinksGroup>
      </PageHeader>
      <PageContentWrapper className={className}>{children}</PageContentWrapper>
    </PageBaseStyled>
  );
}

export default PageBase;
