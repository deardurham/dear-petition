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
import { DropdownMenu } from '../elements/DropdownMenu';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCaretDown, faExternalLinkAlt } from '@fortawesome/free-solid-svg-icons';

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

const PageBaseCentered = styled.div`
  max-width: 1200px;
  width: 100%;
`;

function PageBase({ children, className, ...props }) {
  const history = useHistory();
  const { user } = useAuth();
  const dispatch = useDispatch();
  const [logout] = useLogoutMutation();

  return (
    <PageBaseStyled {...props}>
      <PageBaseCentered>
        <PageHeader>
          <LogoLink>
            <Link to="/">
              <PageLogo src={dearLogo} alt="DEAR logo" />
            </Link>
          </LogoLink>
          <LinksGroup>
            {user && (
              <LinkWrapper>
                <Link to="/">Dashboard</Link>
              </LinkWrapper>
            )}
            <LinkWrapper>
              <Link to="/help">Help</Link>
            </LinkWrapper>
            {user?.is_admin ? (
              <DropdownMenu
                items={[
                  <Link to="/agencies">
                    <LinkWrapper>Agencies</LinkWrapper>
                  </Link>,
                  <Link to="/users">
                    <LinkWrapper>Users</LinkWrapper>
                  </Link>,
                  <a href={user.admin_url} target="_blank" rel="noreferrer">
                    <LinkWrapper>
                      <div className="flex gap-2 items-baseline">
                        <span>Admin</span>
                        <FontAwesomeIcon className="text-[14px]" icon={faExternalLinkAlt} />
                      </div>
                    </LinkWrapper>
                  </a>,
                ]}
              >
                <LinkWrapper>
                  <div className="flex gap-2">
                    <span>Manage</span>
                    <FontAwesomeIcon className="text-[20px]" icon={faCaretDown} />
                  </div>
                </LinkWrapper>
              </DropdownMenu>
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
      </PageBaseCentered>
    </PageBaseStyled>
  );
}

export default PageBase;
