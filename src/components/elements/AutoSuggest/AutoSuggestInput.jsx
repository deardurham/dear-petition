import cx from 'classnames';
import { faSearch } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import React from 'react';
import Input from '../Input/Input';

const AutoSuggestInput = (inputProps, ref) => (
  <div className="flex gap-2">
    <FontAwesomeIcon
      className={cx('self-center text-primary', { 'mt-6': inputProps?.label })}
      icon={faSearch}
    />
    <Input {...inputProps} ref={ref} />
  </div>
);

export default React.forwardRef(AutoSuggestInput);
