import React from 'react';
import { useController } from 'react-hook-form';
import { InputWrapper, InputStyled, ActualInputStyled, InputErrors } from './Input.styled';
import { AnimatePresence } from 'framer-motion';

function FormInput({ className, label, errors, inputProps, ...restProps }) {
  const { field } = useController(inputProps);
  return (
    <InputWrapper className={className}>
      <InputStyled>{label}</InputStyled>
      <ActualInputStyled {...field} {...restProps} />
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

export default FormInput;
