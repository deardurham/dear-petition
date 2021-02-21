import styled from 'styled-components';
import { motion } from 'framer-motion';

export const FilesListWrapper = styled.div`
  width: 350px;
  overflow-y: hidden;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  margin: 2rem 0rem;
`;

export const FilesListStyled = styled.ul`
  margin-top: 1rem;
`;

export const FilesListItem = styled(motion.li)`
  display: flex;
  flex-direction: row;
  align-items: center;
  margin: 1rem 0;

  p {
    flex: 1;
    padding-right: 1rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
`;
