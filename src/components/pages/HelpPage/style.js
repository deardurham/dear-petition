import ReactMarkdown from 'react-markdown';
import styled from 'styled-components';
import { colorPrimary, colorWhite } from '../../../styles/colors';

export const Markdown = styled(ReactMarkdown)`
  & h1,
  & h2,
  & h3,
  & h6 {
    user-select: none;
    font-weight: 600;
    margin-bottom: 0.75rem;
  }
  & p,
  & li,
  & ul {
    font-size: 1.75rem;
    margin-bottom: 1rem;
  }
  & section {
    margin-bottom: 2rem;
  }
  & h1 {
    font-size: 2.75rem;
    margin-bottom: 1.5rem;
  }
  & h2 {
    font-size: 2rem;
  }
  & h3 {
    font-size: 1.5rem;
  }
  & ul {
    list-style: inside disc;
    margin-top: 0.5rem;
  }
  & ol {
    list-style: inside decimal;
    margin-top: 0.5rem;
  }
  & li {
    display: list-item;
    margin-left: 2rem;
  }
  & h1 a {
    display: block;
    padding: 1rem 2rem;
    width: 30rem;
    background-color: ${colorPrimary};
    color: ${colorWhite};
    border-radius: 0.75rem;
  }
`;

export const ExpandableHeader = styled.div`
  display: flex;
  align-items: baseline;
  margin-right: auto;
  gap: 1rem;
  cursor: pointer;
  & h6 {
    font-size: 2rem;
    user-select: none;
  }
`;
