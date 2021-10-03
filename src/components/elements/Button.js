import PropTypes from 'prop-types';
import styled, { css } from 'styled-components';
import keyAndAmbientShadows from '../../styles/shadows';
import { colorPrimary, colorWhite, colorCaution } from '../../styles/colors';
import { fontPrimary } from '../../styles/fonts';

export const Button = styled.button`
  cursor: pointer;
  ${({ type }) => mapTypeToStartingState(type)}

  border-radius: 3px;
  padding: 0.25rem;
  outline: none;

  font-size: inherit;
  font-family: ${fontPrimary};

  ${keyAndAmbientShadows.dp2};

  &:hover {
    ${keyAndAmbientShadows.dp2};
  }

  &:active {
    ${keyAndAmbientShadows.dp2};
  }
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

function mapTypeToStartingState(type) {
  switch (type) {
    case POSITIVE:
      return positive;
    case CAUTION:
      return caution;
    case NEUTRAL:
      return neutral;
    default:
      return positive;
  }
}

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
  type: PropTypes.oneOf([POSITIVE, CAUTION, NEUTRAL]),
  /** What happens when the button is clicked */
  onClick: PropTypes.func.isRequired,
};

Button.defaultProps = {
  type: POSITIVE,
};
