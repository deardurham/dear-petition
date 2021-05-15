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
  justify-content: center;
  align-items: center;
`;

const HelpPageContent = styled.div`
  width: 75%;
  max-width: 1200px;
  min-width: 400px;
`;

const getHeaderAnchor = heading => {
  let anchor = typeof heading === 'string' ? heading.toLowerCase() : '';
  anchor = anchor.replace(/[^a-zA-Z0-9 ]/g, '');
  anchor = anchor.replace(/ /g, '-');
  return `${anchor}`;
};

const AnchorWrapper = ({ anchor, children }) => (
  <a id={anchor} href={`#${anchor}`}>
    <span>{children}</span>
  </a>
);

const ExpandableSection = ({ children }) => {
  let expandable = false;
  const [isExpanded, setIsExpanded] = useState(false);
  return (
    <section>
      {children.map((child) => {
        if (child?.type === 'h6') {
          expandable = true;
          return (
            <ExpandableHeader onClick={() => expandable && setIsExpanded(prev => !prev)}>
              {child}
              <FontAwesomeIcon icon={isExpanded ? faCaretRight : faCaretDown} />
            </ExpandableHeader>
          );
        } else {
          return !expandable || isExpanded ? child : null;
        }
      })}
    </section>
  );
};

export default function HelpPage() {
  const [source, setSource] = useState();
  useEffect(() => {
    fetch(markdownSource)
      .then(res => res.text())
      .then(text => setSource(text));
  }, [source]);
  return (
    <HelpPageStyled>
      <HelpPageContent>
        <Markdown
          remarkPlugins={[sectionize]}
          components={{
            h1: ({ node, children, ...props }) => (
              <h1 {...props}>
                <AnchorWrapper anchor={getHeaderAnchor(children.join(' '))}>
                  <span>{children}</span>
                </AnchorWrapper>
              </h1>
            ),
            section: ({ children }) => <ExpandableSection>{children}</ExpandableSection>
          }}
        >
          {source}
        </Markdown>
      </HelpPageContent>
    </HelpPageStyled>
  );
}
