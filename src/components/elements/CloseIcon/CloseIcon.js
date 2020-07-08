import React from 'react';
import { CloseIconStyled } from './CloseIcon.styled';
import { faTimes } from '@fortawesome/free-solid-svg-icons';

export default function({ onClose }) {
    return <CloseIconStyled onClick={onClose} icon={faTimes} />
};
