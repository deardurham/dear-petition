import PropTypes from 'prop-types';
import styled, { css } from 'styled-components';
import keyAndAmbientShadows from '../../../styles/shadows';
import { colorPrimary, colorWhite, colorCaution, greyScale } from '../../../styles/colors';
import { fontPrimary } from '../../../styles/fonts';

export const Button = styled.button`
  cursor: pointer;
  ${({ colorClass }) => mapTypeToStartingState(colorClass)}
  ${({ disabled }) => disabled && mapTypeToStartingState(DISABLED)}
  border-radius: 3px;
  padding: 0.5rem;
  outline: none;

  font-size: inherit;
  font-family: ${fontPrimary};

  box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
`;

export const CloseButton = styled(Button)`
  padding: 0 0.25rem;
  border-radius: 0;
  transition: none;
  transform: none;
  font-size: 1.25rem;
  ${keyAndAmbientShadows.dp1};

  &:hover {
    transform: none;
    ${keyAndAmbientShadows.dp1};
  }

  &:active {
    transform: none;
  }
`;

export const POSITIVE = 'positive';
export const CAUTION = 'caution';
export const NEUTRAL = 'neutral';
export const DISABLED = 'disabled';

function mapTypeToStartingState(colorClass) {
  switch (colorClass) {
    case POSITIVE:
      return positive;
    case CAUTION:
      return caution;
    case NEUTRAL:
      return neutral;
    case DISABLED:
      return disabled;
    default:
      return positive;
  }
}

const disabled = css`
  background: ${greyScale(7.25)};
  border: 1px solid ${greyScale(7.25)};
  color: ${colorWhite};
`;
const positive = css`
  background: ${colorPrimary};
  border: 1px solid ${colorPrimary};
  color: ${colorWhite};
`;
const caution = css`
  background: ${colorCaution};
  border: 1px solid ${colorCaution};
  color: ${colorWhite};
`;

const neutral = css`
  background: ${colorWhite};
  border: 1px solid ${colorPrimary};
  color: ${colorPrimary};
`;

Button.propTypes = {
  /** Reflects the state of the button */
  colorClass: PropTypes.oneOf([POSITIVE, CAUTION, NEUTRAL, DISABLED]),
  /** What happens when the button is clicked */
  onClick: PropTypes.func.isRequired,
};

Button.defaultProps = {
  colorClass: POSITIVE,
};
