import React from 'react';
import PropTypes from 'prop-types';
import { SelectStyled, ActualSelectStyled, OptionStyled } from './Select.styled';

function Select({ value, onChange, label, options }) {
  return (
    <SelectStyled>
      {label}
      <ActualSelectStyled value={value} onChange={onChange}>
        {options.map(option => {
          return (
            <OptionStyled key={option.value} value={option.value}>
              {option.name}
            </OptionStyled>
          );
        })}
      </ActualSelectStyled>
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
