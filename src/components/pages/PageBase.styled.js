import styled from 'styled-components';
import { motion } from 'framer-motion';
import { colorGrey, colorBlack } from '../../styles/colors';
import { smallerThanTabletLandscape } from '../../styles/media';

export const PageBaseStyled = styled(motion.main)`
  flex: 1;
  display: flex;
  flex-direction: column;
`;

export const PageHeader = styled.header`
  padding: 0 4rem;
  font-size: 1.75rem;
  font-weight: bold;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  @media (${smallerThanTabletLandscape}) {
    padding-top: 2rem;
    flex-direction: column;
    justify-content: flex-start;
    align-items: center;
  }
`;

export const PageLogo = styled.img`
  width: 100%;
  height: 100%;
`;

export const LinksGroup = styled.div`
  flex: 1;
  display: flex;
  justify-content: flex-end;
  a:not(:first-child) {
    margin-left: 1rem;
  }
  @media (${smallerThanTabletLandscape}) {
    margin-top: 2rem;
  }
`;

export const Link = styled.a`
  border: 1px solid ${colorBlack};
  border-radius: 5px;
  padding: 2rem;
  color: ${colorGrey};
`;

export const PageContentWrapper = styled.section`
  padding: 2rem 4rem;
  flex: 1;
  @media (${smallerThanTabletLandscape}) {
    padding: 2rem;
  }
`;
