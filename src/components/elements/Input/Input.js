import React from 'react';
import PropTypes from 'prop-types';
import { InputWrapper, InputStyled, ActualInputStyled, InputErrors } from './Input.styled';
import { AnimatePresence } from 'framer-motion';

function Input({ className, label, errors, register, name, ...inputProps }) {
  const registerProps = register && name ? { ...register(name) } : {};
  return (
    <InputWrapper className={className}>
      <InputStyled>{label}</InputStyled>
      <ActualInputStyled {...inputProps} {...registerProps} />
      {errors && (
        <AnimatePresence>
          <InputErrors
            initial={{ opacity: 0, y: -25 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: '50' }}
            positionTransition
          >
            {errors && errors.map((errMsg) => <p key={errMsg}>{errMsg}</p>)}
          </InputErrors>
        </AnimatePresence>
      )}
    </InputWrapper>
  );
}

export default Input;
