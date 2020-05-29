import React from 'react';
import { BadgeStyled, IconStyled, AutoCompleteBadgeStyled } from './Badge.styled';

const AutoCompleteBadge = ({ name, ...props }) => {
    return (
        <AutoCompleteBadgeStyled {...props} data-cy="badge">
            <p>{name}</p>
        </AutoCompleteBadgeStyled>
    );
};

const Badge = ({ name, remove, ...props }) => {
    return (
        <BadgeStyled {...props} data-cy="badge">
            <p>{name}</p>
            {remove && (
                <IconStyled onClick={remove} data-cy="badge_close">
                    x
                </IconStyled>
            )}
        </BadgeStyled>
    );
};

export { Badge, AutoCompleteBadge };
