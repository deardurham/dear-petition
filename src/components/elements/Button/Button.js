import React from 'react';
import PropTypes from 'prop-types';
import ButtonStyled from './Button.styled';

export default function Button({ children, ...props }) {
  return <ButtonStyled {...props}>{children}</ButtonStyled>;
}

/* Props */
export const POSITIVE = 'positive';
export const CAUTION = 'caution';
export const NEUTRAL = 'neutral';

Button.propTypes = {
  /** Reflects the state of the button */
  type: PropTypes.oneOf([POSITIVE, CAUTION, NEUTRAL]),
  /** What happens when the button is clicked */
  onClick: PropTypes.func.isRequired,
};

Button.defaultProps = {
  type: POSITIVE,
};
