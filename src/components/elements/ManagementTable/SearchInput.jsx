import { useState } from 'react';
import cx from 'classnames';

import useDebounce from '../../../hooks/useDebounce';
import { Button } from '../Button';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSearch } from '@fortawesome/free-solid-svg-icons';

const SearchInput = ({ className, onSearch, placeholder }) => {
  const [formValue, setFormValue] = useState('');
  const debounceSearch = useDebounce((value) => onSearch(value), { timeout: 400 });
  return (
    <div className="flex gap-2">
      <FontAwesomeIcon className="self-center text-primary" icon={faSearch} />
      <input
        type="search"
        className={cx('px-3 rounded border border-1 border-gray', className)}
        placeholder={placeholder}
        value={formValue}
        onChange={(e) => {
          const text = e.target.value;
          setFormValue(text);
          debounceSearch(text);
        }}
      />
      {formValue && (
        <Button
          colorClass="neutral"
          className="px-2 py-1 border border-gray-700 rounded-md shadow-md font-semibold"
          onClick={() => {
            setFormValue('');
            onSearch('');
          }}
        >
          Clear
        </Button>
      )}
    </div>
  );
};

export default SearchInput;
