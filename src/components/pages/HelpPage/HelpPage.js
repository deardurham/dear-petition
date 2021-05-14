import React, { useEffect, useState } from 'react';
import styled from 'styled-components';
import ReactMarkdown from 'react-markdown';
import PageBase from '../PageBase';
import markdownSource from './help.md';

const Markdown = styled(ReactMarkdown)`
  h1 {
    font-size: 2.75rem;
  }
  h2 {
    font-size: 2rem;
    margin-bottom: 1rem;
  }
  & > * {
    margin-bottom: 2rem;
  }
  ul {
    list-style: inside disc;
    margin-top: 0.5rem;
  }
  li {
    display: list-item;
    margin-left: 2rem;
    margin-bottom: 0.5rem;
  }
`;

export const HelpPageStyled = styled(PageBase)`
  display: flex;
  justify-content: center;
  align-items: center;
`;

const HelpPageContent = styled.div`
  width: 75%;
  max-width: 1200px;
  min-width: 400px;
`;

export default function HelpPage() {
  const [source, setSource] = useState();
  useEffect(() => {
    fetch(markdownSource)
      .then(res => res.text())
      .then(text => setSource(text));
  });
  return (
    <HelpPageStyled>
      <HelpPageContent>
        <Markdown>{source}</Markdown>
      </HelpPageContent>
    </HelpPageStyled>
  );
}
