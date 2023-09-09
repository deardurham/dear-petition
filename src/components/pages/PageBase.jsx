import { useDispatch } from 'react-redux';
import { Link, useHistory } from 'react-router-dom';
import styled from 'styled-components';
import {
  LinkWrapper,
  LinksGroup,
  PageBaseStyled,
  PageHeader,
  PageFooter,
  Logo,
  PageContentWrapper,
} from './PageBase.styled';
import dearLogo from '../../assets/img/DEAR_logo.png';
import codeWithDurhamHorizontalLogo from '../../assets/img/CWD_horizontal_logo.png';
import { smallerThanTabletLandscape } from '../../styles/media';

import useAuth from '../../hooks/useAuth';
import { useLogoutMutation } from '../../service/api';
import { loggedOut } from '../../slices/auth';
import { DropdownMenu } from '../elements/DropdownMenu';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCaretDown, faExternalLinkAlt } from '@fortawesome/free-solid-svg-icons';

const HeaderLogoLink = styled(LinkWrapper)`
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
const FooterLogoLink = styled(LinkWrapper)`
  border: none;
  padding: 0;
  width: 200px;
  height: auto;
`;

const LogoutLink = styled(LinkWrapper)`
  cursor: pointer;
`;

const PageBaseCentered = styled.div`
  max-width: 1200px;
  width: 100%;
  flex: 1;
  display: flex;
  flex-direction: column;
`;

function PageBase({ children, className, ...props }) {
  const history = useHistory();
  const { user } = useAuth();
  const dispatch = useDispatch();
  const [logout] = useLogoutMutation();
  let bookmarkletJS = `var username=prompt("Enter your Durham Expunction username"),html=document.documentElement.innerHTML,loaded=0,iframe=document.createElement("iframe");iframe.name="bookmarklet-"+Math.floor(1e4*Math.random()+1),iframe.style.display="none",iframe.onload=function(){1!=++loaded&&document.body.removeChild(iframe)};var form=document.createElement("form");form.method="POST",form.action="https://27a9-99-92-50-211.ngrok-free.app/portal/bookmarklet/?nocache="+Math.random(),form.target=iframe.name;var username_input=document.createElement("input");username_input.name="user",username_input.value=username;var textarea=document.createElement("textarea");textarea.name="source",textarea.value=html,form.appendChild(username_input),form.appendChild(textarea),iframe.appendChild(form),document.body.appendChild(iframe),form.submit();`;
  let bookmarklet = `javascript:(function(){${bookmarkletJS}})()`;

  return (
    <PageBaseStyled {...props}>
      <PageBaseCentered>
        <PageHeader>
          <HeaderLogoLink>
            <Link to="/">
              <Logo src={dearLogo} alt="DEAR logo" />
            </Link>
          </HeaderLogoLink>
          <LinksGroup>
            {user && (
              <LinkWrapper>
                <Link to="/">Dashboard</Link>
              </LinkWrapper>
            )}
            <LinkWrapper>
              <Link to="/help">Help</Link>
            </LinkWrapper>
            <LinkWrapper>
              <a href={bookmarklet} title="Drag to your bookmarks bar">Portal Importer (beta)</a>
            </LinkWrapper>
            {user?.is_admin ? (
              <DropdownMenu
                items={[
                  <Link key="agencies" to="/agencies">
                    <LinkWrapper>Agencies</LinkWrapper>
                  </Link>,
                  <Link key="users" to="/users">
                    <LinkWrapper>Users</LinkWrapper>
                  </Link>,
                  <a key="admin" href={user.admin_url} target="_blank" rel="noreferrer">
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
        <PageFooter>
          <FooterLogoLink>
            <p className="m-0 relative top-14 text-[1.25rem] text-center">developed by</p>
            <a href="https://www.codefordurham.com/" target="_blank" rel="noopener noreferrer">
              <Logo src={codeWithDurhamHorizontalLogo} alt="Code with Durham logo" />
            </a>
          </FooterLogoLink>
        </PageFooter>
      </PageBaseCentered>
    </PageBaseStyled>
  );
}

export default PageBase;
