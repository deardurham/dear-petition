import React from 'react';
import styled from 'styled-components';
import { useController } from 'react-hook-form';
import { InputWrapper, InputStyled, ActualInputStyled, InputErrors } from './Input.styled';
import { AnimatePresence } from 'framer-motion';

const ActualInputRestyled = styled(ActualInputStyled)`
  width: 100%;
  padding: 0.5rem;
`;

const InputRestyled = styled(InputStyled)`
  width: 100%;
`;

const FormInput = ({ className, label, errors, inputProps, ...restProps }) => {
  const { field, fieldState } = useController(inputProps);
  const { error: inputError } = fieldState;
  const error = inputError ? (
    <p>Invalid value</p>
  ) : (
    errors?.map((errMsg, i) => <p key={`${i}${errMsg}`}>{errMsg}</p>)
  );
  return (
    <InputWrapper className={className}>
      <InputRestyled>{label}</InputRestyled>
      <ActualInputRestyled type="input" {...field} {...restProps} />
      {error && (
        <AnimatePresence>
          <InputErrors
            initial={{ opacity: 0, y: -25 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: '50' }}
            positionTransition
          >
            {error}
          </InputErrors>
        </AnimatePresence>
      )}
    </InputWrapper>
  );
};

export default FormInput;
