import styled from 'styled-components';
import { motion } from 'framer-motion';

export const FilesListWrapper = styled.div`
  height: 420px;
  width: 350px;
  overflow-y: hidden;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  margin-bottom: 2rem;
`;

export const FilesListStyled = styled.ul`
  overflow-y: scroll;
`;

export const FilesListItem = styled(motion.li)`
  display: flex;
  flex-direction: row;
  align-items: center;

  p {
    flex: 1;
    padding-right: 1rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  span {
    cursor: pointer;
  }
`;
