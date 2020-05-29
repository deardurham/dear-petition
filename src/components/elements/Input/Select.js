import React from 'react';
import PropTypes from 'prop-types';
import { SelectWrapper, SelectStyled, ActualSelectStyled, InputErrors } from './Select.styled';
import { AnimatePresence } from 'framer-motion';

function Select({ value, onChange, label, errors, options }) {
  return (
    <SelectWrapper>
      <SelectStyled>
        {label}
        <ActualSelectStyled value={value} options={options} onChange={onChange} />
      </SelectStyled>
      <AnimatePresence>
        <InputErrors
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: '-50' }}
          positionTransition
        >
          {errors && errors.map(errMsg => <p key={errMsg}>{errMsg}</p>)}
        </InputErrors>
      </AnimatePresence>
    </SelectWrapper>
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
