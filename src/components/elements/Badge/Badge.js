import cx from 'classnames';
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
  <div className="flex items-center justify-between gap-3 rounded-md bg-gray-600 px-2 py-1 text-gray-100">
    <p title={name} className="text-lg text-inherit max-w-[200px] truncate">
      {name}
    </p>
    {remove && (
      <button
        type="button"
        className="outline-white outline-offset-2 hover:outline-dotted hover:outline-[1px]"
        onClick={remove}
        onKeyDown={(e) => e?.code === 13 && remove()}
      >
        <FontAwesomeIcon icon={faTimes} />
      </button>
    )}
  </div>
);

export { Badge, AutoCompleteBadge };
