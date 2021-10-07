import React from 'react';
import PropTypes from 'prop-types';
import { InputWrapper, InputStyled, ActualInputStyled, InputErrors } from './Input.styled';
import { AnimatePresence } from 'framer-motion';

function Input({ value, onChange, label, type, errors, maxLength, disabled, ...props }) {
  return (
    <InputWrapper {...props}>
      <InputStyled>
        {label}
        <ActualInputStyled
          type={type}
          maxLength={maxLength}
          value={value}
          onChange={onChange}
          disabled={disabled}
        />
      </InputStyled>
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
    </InputWrapper>
  );
}

Input.propTypes = {
  value: PropTypes.string,
  onChange: PropTypes.func,
  label: PropTypes.string,
};

Input.defaultProps = {
  value: '',
  label: '',
  onChange: () => {},
};

export default Input;
