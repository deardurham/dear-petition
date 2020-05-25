import styled from 'styled-components';
import { colorGrey, colorGreyLight, colorBlack } from '../../../styles/colors';

const getBadgeColor = props => {
  let baseColor = colorGreyLight;
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

  background-color: ${props => getBadgeColor(props)};
`;

const BadgeStyled = styled.div`
  max-width: 100%;
  height: 1.6rem;
  display: flex;
  flex-direction: row;
  align-items: flex-end;
  justify-content: space-between;

  margin: 0 2px 2px 0;
  border-radius: 1px;
  padding: 10px 0px;

  p:first-of-type {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    padding: 0 1.5rem;
    margin: 0;

    color: ${colorBlack};
    font-size: 1.5rem;
  }

  background-color: ${colorGreyLight};
`;

const IconStyled = styled.p`
  color: ${colorBlack};
  font-size: 1rem;
  margin-left: 1rem;
  align-self: center;
  cursor: pointer;
  padding-right: 0.6rem;

  &:hover {
    color: ${colorGreyLight};
  }
`;

export { AutoCompleteBadgeStyled, BadgeStyled, IconStyled };
