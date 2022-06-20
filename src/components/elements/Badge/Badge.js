import React from 'react';
import { BadgeStyled, IconStyled, AutoCompleteBadgeStyled } from './Badge.styled';

const AutoCompleteBadge = ({ name, ...props }) => (
  <AutoCompleteBadgeStyled {...props} data-cy="badge">
    <p>{name}</p>
  </AutoCompleteBadgeStyled>
);

const Badge = ({ name, remove }) => (
  <BadgeStyled>
    <p>{name}</p>
    {remove && <IconStyled onClick={remove}>x</IconStyled>}
  </BadgeStyled>
);

export { Badge, AutoCompleteBadge };
