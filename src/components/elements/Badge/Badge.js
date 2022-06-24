import { faTimes } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import React from 'react';
import { AutoCompleteBadgeStyled } from './Badge.styled';

const AutoCompleteBadge = ({ name, ...props }) => (
  <AutoCompleteBadgeStyled {...props} data-cy="badge">
    <p>{name}</p>
  </AutoCompleteBadgeStyled>
);

const Badge = ({ name, remove }) => (
  <div className="flex items-center justify-between gap-3 rounded-md bg-gray-600 px-2 py-1">
    <p className="text-gray-100 text-lg">{name}</p>
    {remove && (
      <FontAwesomeIcon
        className="text-gray-100 hover:text-gray-800 cursor-pointer"
        onClick={remove}
        icon={faTimes}
      />
    )}
  </div>
);

export { Badge, AutoCompleteBadge };
