import React from 'react';
import cx from 'classnames';

const SPINNER_SIZES = {
  xs: 'w-6 h-6',
  sm: 'w-10 h-10',
  base: 'w-12 h-12',
  lg: 'w-16 h-16',
  '2xl': 'w-24 h-24',
};

export const Spinner = ({ size }) => (
  <div
    className={cx(
      'animate-spin',
      'p-0',
      'text-primary border-primary',
      'border-t-2 border-l-2 rounded-full',
      SPINNER_SIZES?.[size] ? SPINNER_SIZES[size] : SPINNER_SIZES.base
    )}
  />
);
