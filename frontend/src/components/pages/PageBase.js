import React from 'react';
import {
  PageBaseStyled,
  PageHeader,
  PageLogo,
  PageContentWrapper,
} from "./PageBase.styled";
import DEAR_Logo from '../../assets/img/DEAR_logo.png';

function PageBase({ children, ...props }) {
  return (
    <PageBaseStyled {...props}>
      <PageHeader>
        <PageLogo>
          <img src={DEAR_Logo} alt="DEAR logo" />
        </PageLogo>
      </PageHeader>
      <PageContentWrapper>{children}</PageContentWrapper>
    </PageBaseStyled>
  );
}

export default PageBase;
