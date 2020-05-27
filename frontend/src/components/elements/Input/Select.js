import React from 'react';
import PropTypes from 'prop-types';
import { SelectStyled, ActualSelectStyled, OptionStyled } from './Select.styled';

function Select({ value, onChange, label, options }) {
  return (
    <SelectStyled>
      {label}
      <ActualSelectStyled value={value} options={options} onChange={onChange} />
    </SelectStyled>
  );
}

Select.propTypes = {
  value: PropTypes.any.isRequired,
  onChange: PropTypes.func.isRequired,
  label: PropTypes.string,
  options: PropTypes.array.isRequired
};

Select.defaultProps = {
  options: []
};

export default Select;
