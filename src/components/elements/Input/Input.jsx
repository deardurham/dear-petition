import React from 'react';
import { InputWrapper, InputStyled, ActualInputStyled, InputErrors, InputWarnings } from './Input.styled';
import { AnimatePresence } from 'framer-motion';

function Input({ className, innerClassName, label, errors, warnings, register, name, type, ...inputProps }, ref) {
  const registerProps = register && name ? { ...register(name) } : {};

  const errorAnimateProps = {
    initial: { opacity: 0, y: -25 },
    animate: { opacity: 1, y: 0 },
    exit: { opacity: 0, y: '50' },
    positionTransition: true,
  };

  return (
    <InputWrapper className={className}>
      <InputStyled>{label}</InputStyled>
      <ActualInputStyled className={innerClassName} type={type} {...inputProps} {...registerProps} ref={ref} />
      <AnimatePresence>
        {errors && (
          <InputErrors key="input-errors" {...errorAnimateProps}>
            {errors && errors.map((errMsg) => <p key={errMsg}>{errMsg}</p>)}
          </InputErrors>
        )}
        {warnings && (
          <InputWarnings key="input-warnings" {...errorAnimateProps}>
            {warnings.map((warningMsg) => (
              <p key={warningMsg}>{warningMsg}</p>
            ))}
          </InputWarnings>
        )}
      </AnimatePresence>
    </InputWrapper>
  );
}

export default React.forwardRef(Input);
