import styled from 'styled-components';
import { colorGrey, colorBlack, greyScale } from '../../../styles/colors';

const getBadgeColor = (props) => {
  const baseColor = greyScale(9);
  return props.isHighlighted ? colorGrey : baseColor;
};

const AutoCompleteBadgeStyled = styled.div`
  max-width: 100%;
  display: flex;
  flex-direction: row;
  justify-content: space-between;

  margin: 0 2px 2px 0;
  border-radius: 1px;
  cursor: pointer;

  p:first-of-type {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    padding: 0 1.5rem;

    color: ${colorBlack};
    font-size: 1.5rem;
    font-weight: bold;
  }

  background-color: ${(props) => getBadgeColor(props)};
`;

export { AutoCompleteBadgeStyled };
