import styled from 'styled-components';
import { motion } from 'framer-motion';
import { colorGrey } from '../../styles/colors';

export const PageBaseStyled = styled(motion.main)`
  flex: 1;
  display: flex;
  flex-direction: column;
`;

export const PageHeader = styled.header`
  padding: 4rem;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: flex-start;
`;

export const PageLogo = styled.div`
  flex: 1;
  img {
    width: 260px;
  }
`;

export const AdminButton = styled.a`
  margin: 0 1rem;
  border: none;
  color: ${colorGrey};
`;

export const LogoutButton = styled.button`
  margin: 0 1rem;
  border: none;
  color: ${colorGrey};
  cursor: pointer;
`;

export const PageContentWrapper = styled.section`
  flex: 1;
  display: flex;
`;
