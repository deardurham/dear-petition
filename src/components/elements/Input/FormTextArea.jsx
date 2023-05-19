import cx from 'classnames';
import { useController } from 'react-hook-form';
import { AnimatePresence } from 'framer-motion';
import { InputErrors } from './Input.styled';

const FormTextArea = ({ className, label, rows, errors, inputProps }) => {
  const { field, fieldState } = useController(inputProps);
  const { onChange, ...fieldProps } = field;
  const { error: inputError } = fieldState;
  const error = inputError ? (
    <p>Invalid value</p>
  ) : (
    errors?.map((errMsg, i) => <p key={`${i}${errMsg}`}>{errMsg}</p>)
  );
  const textAreaOnChange = (e) => {
    if (e.target.value?.split('\n').length <= rows) {
      onChange(e);
    }
  };
  return (
    <div>
      <label className="flex flex-col text-[1.4rem] select-none">
        {label}
        <textarea
          className={cx('resize-none rounded-[5px] text-sm p-2 border border-gray', className)}
          onChange={textAreaOnChange}
          {...fieldProps}
        />
      </label>
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
    </div>
  );
};

export default FormTextArea;
