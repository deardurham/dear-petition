import React, { useEffect, useState } from 'react';
import styled from 'styled-components';
import PageBase from '../PageBase';
import markdownSource from './help.md';
import sectionize from 'remark-sectionize';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCaretDown, faCaretRight } from '@fortawesome/free-solid-svg-icons';
import { Markdown, ExpandableHeader } from './style';

export const HelpPageStyled = styled(PageBase)`
  display: flex;
`;

const HelpPageContent = styled.div`
  width: 75%;
  max-width: 1200px;
  min-width: 400px;
`;

const ExpandableSection = ({ children }) => {
  let expandable = false;
  const [isExpanded, setIsExpanded] = useState(true);
  return (
    <section>
      {children.map((child) => {
        if (child?.type === 'h6') {
          expandable = true;
          return (
            <ExpandableHeader onClick={() => expandable && setIsExpanded((prev) => !prev)}>
              {child}
              <FontAwesomeIcon icon={isExpanded ? faCaretRight : faCaretDown} />
            </ExpandableHeader>
          );
        }
        return !expandable || isExpanded ? child : null;
      })}
    </section>
  );
};

export default function HelpPage() {
  const [source, setSource] = useState();
  useEffect(() => {
    fetch(markdownSource)
      .then((res) => res.text())
      .then((text) => setSource(text));
  }, [source]);
  return (
    <HelpPageStyled>
      <HelpPageContent>
        <Markdown
          remarkPlugins={[sectionize]}
          components={{
            section: ({ children }) => <ExpandableSection>{children}</ExpandableSection>,
          }}
        >
          {source}
        </Markdown>
      </HelpPageContent>
    </HelpPageStyled>
  );
}
