import React from 'react';
import PropTypes from 'prop-types';
import { SelectWrapper, SelectStyled, ActualSelectStyled, InputErrors } from './Select.styled';
import { AnimatePresence } from 'framer-motion';

function Select({ value, onChange, label, errors, options, disabled, className }) {
  // const { state } = value;
  // const stateObj = {
  //   state: value,
  // };
  console.log(`value prop as passed into Select:`, value);
  // console.log(`stateObj from Select`, typeof stateObj, stateObj);
  return (
    <SelectWrapper className={className}>
      <SelectStyled>
        {label}
        <ActualSelectStyled
          value={value}
          options={options}
          onChange={onChange}
          isDisabled={disabled}
        />
      </SelectStyled>
      <AnimatePresence>
        <InputErrors
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: '-50' }}
          positionTransition
        >
          {errors && errors.map((errMsg) => <p key={errMsg}>{errMsg}</p>)}
        </InputErrors>
      </AnimatePresence>
    </SelectWrapper>
  );
}

Select.propTypes = {
  value: PropTypes.shape({
    value: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
    label: PropTypes.string,
  }).isRequired,
  onChange: PropTypes.func.isRequired,
  label: PropTypes.string,
  options: PropTypes.arrayOf(
    PropTypes.shape({
      value: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
      label: PropTypes.string,
    })
  ).isRequired,
};

Select.defaultProps = {
  label: '',
};

export default Select;
