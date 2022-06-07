import React from 'react';
import { AnimatePresence } from 'framer-motion';
import { useController } from 'react-hook-form';

import { SelectWrapper, SelectStyled, ActualSelectStyled, InputErrors } from './Select.styled';

const FormSelect = ({ className, disabled, label, options, errors, inputProps }) => {
  const { field, fieldState } = useController(inputProps);
  const { error: inputError } = fieldState;
  const error = inputError ? (
    <p>Invalid value</p>
  ) : (
    errors?.map((errMsg, i) => <p key={`${i}${errMsg}`}>{errMsg}</p>)
  );
  return (
    <SelectWrapper className={className}>
      <SelectStyled>
        {label}
        <ActualSelectStyled {...field} isDisabled={disabled} options={options} />
      </SelectStyled>
      {error && (
        <AnimatePresence>
          <InputErrors
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: '-50' }}
            positionTransition
          >
            {error}
          </InputErrors>
        </AnimatePresence>
      )}
    </SelectWrapper>
  );
};

export default FormSelect;
