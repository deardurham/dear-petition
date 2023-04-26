import React from 'react';
import cx from 'classnames';
import { NEUTRAL, POSITIVE } from './Button/Button';

const SPINNER_SIZES = {
  '2xs': 'w-6 h-6',
  xs: 'w-8 h-8',
  sm: 'w-10 h-10',
  base: 'w-12 h-12',
  lg: 'w-16 h-16',
  '2xl': 'w-24 h-24',
};

const SPINNER_COLORS = {
  [NEUTRAL]: 'text-primary border-primary',
  [POSITIVE]: 'text-white border-white',
};

export const Spinner = ({ size, color }) => (
  <div
    className={cx(
      'animate-spin',
      'p-0',
      'border-t-2 border-l-2 rounded-full',
      SPINNER_SIZES?.[size] ? SPINNER_SIZES[size] : SPINNER_SIZES.base,
      SPINNER_COLORS?.[color] ? SPINNER_COLORS[color] : SPINNER_COLORS[NEUTRAL]
    )}
  />
);
