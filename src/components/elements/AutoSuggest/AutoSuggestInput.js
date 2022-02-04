import React from 'react';
import Input from '../Input/Input';

const AutoSuggestInput = (inputProps, ref) => <Input {...inputProps} ref={ref} />;

export default React.forwardRef(AutoSuggestInput);
