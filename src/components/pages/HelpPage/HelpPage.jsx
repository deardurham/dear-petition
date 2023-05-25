import { useEffect, useRef, useState } from 'react';
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
      {children.map((child, i) => {
        if (child?.type === 'h6') {
          expandable = true;
          return (
            <ExpandableHeader
              // TODO: investigate other possible keys. but this is likely a non-issue
              // eslint-disable-next-line react/no-array-index-key
              key={i}
              onClick={() => expandable && setIsExpanded((prev) => !prev)}
            >
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
  const sectionCount = useRef(0);
  useEffect(() => {
    fetch(markdownSource)
      .then((res) => res.text())
      .then((text) => setSource(text));
  }, []);
  return (
    <HelpPageStyled>
      <HelpPageContent>
        <Markdown
          remarkPlugins={[sectionize]}
          components={{
            section: ({ children }) => {
              const key = `${sectionCount.current}`;
              sectionCount.current += 1;
              return <ExpandableSection key={key}>{children}</ExpandableSection>;
            },
          }}
        >
          {source}
        </Markdown>
      </HelpPageContent>
    </HelpPageStyled>
  );
}
