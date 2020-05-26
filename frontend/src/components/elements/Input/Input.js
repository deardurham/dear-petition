import React from 'react';
import PropTypes from 'prop-types';
import { InputStyled, ActualInputStyled } from './Input.styled';

function Input({ value, onChange, label, ...props }) {
  return (
    <InputStyled>
      {label}
      <ActualInputStyled value={value} onChange={onChange} {...props} />
    </InputStyled>
  );
}

Input.propTypes = {
  value: PropTypes.any.isRequired,
  onChange: PropTypes.func.isRequired,
  label: PropTypes.string
};

Input.defaultProps = {};

export default Input;
