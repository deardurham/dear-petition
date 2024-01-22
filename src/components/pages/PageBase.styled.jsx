import styled from 'styled-components';
import { motion } from 'framer-motion';
import { colorBlue, colorBlack, colorGrey } from '../../styles/colors';
import { smallerThanTabletLandscape } from '../../styles/media';

export const PageBaseStyled = styled(motion.main)`
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
	overflow-x: hidden;
	* {
      max-width: 100vw;
    }
`;

export const PageHeader = styled.header`
  padding: 1rem 4rem;
  font-size: 1.75rem;
  font-weight: bold;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  @media (${smallerThanTabletLandscape}) {
    flex-direction: column;
    justify-content: flex-start;
    align-items: center;
	  padding: 2rem 0 0 0;
	  width: 100vw;
  }
`;

export const Logo = styled.img`
  max-width: 100vw;
  height: 100%;
`;

export const LinksGroup = styled.div`
  flex: 1;
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  @media (${smallerThanTabletLandscape}) {
    margin: 2rem 0 0 0;
	  padding: 0;
	  width: 100vw;
	  justify-content: space-evenly;
    background-color: #00919f;
	  div {
		  margin: 1.5rem 0;
		  padding: 1px 3px;
		  align-content: center;
		  justify-content: center;
		  align-items: center;
		  display: flex;
		  height: 2rem;
		  border: transparent;
		  color: white;
		  &.drop {
			  * {
				  width: 15rem;
          background-color: #00919f;
			  }
			  height: 4rem;
			  position: absolute;
			  top: 3rem;
			  flex-direction: column;
		  }
	  }
  }
`;

export const LinkWrapper = styled.div`
  border: 1px solid ${colorBlack};
  border-radius: 5px;
  padding: 1.5rem 1.25rem;
	cursor: pointer;
  color: ${colorGrey};
  & > a {
    color: ${colorGrey};
  }
  & > a:hover,
  &:hover {
    color: ${colorBlue};
  }
  @media (${smallerThanTabletLandscape}) {
	  img {
		  width: 100%;
	  }
    button {
	    padding: 0;
	    margin: 0;
    }
    a {
	    color: white;
    }
  }
`;

export const PageContentWrapper = styled.section`
  padding: 2rem 4rem;
  flex: 1;
  @media (${smallerThanTabletLandscape}) {
    padding: 2rem 1rem;
	  overflow-wrap: break-word;
	  width: 100vw;
	  * {
		  max-width: 95vw;
	  }
  }
	div {
		max-width: 100vw;
	}
`;

export const PageFooter = styled.footer`
  margin-top: 2rem;
  display: flex;
  justify-content: center;
  align-items: center;
`;
