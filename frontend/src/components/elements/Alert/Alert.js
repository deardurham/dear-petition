import React from 'react';
import { AlertStyled, IconStyled, CloseIcon } from './Alert.styled';
import { faExclamationCircle, faTimes } from '@fortawesome/free-solid-svg-icons';
import { faCheckCircle } from '@fortawesome/free-regular-svg-icons';

function Alert({ options, message, close }) {
  const getIconFromType = type => {
    switch (type) {
      case 'info':
        return faExclamationCircle;
      case 'error':
        return faExclamationCircle;
      case 'success':
        return faCheckCircle;
      default:
        return faExclamationCircle;
    }
  };

  return (
    <AlertStyled type={options.type}>
      <IconStyled icon={getIconFromType(options.type)} type={options.type} />
      <p>{message}</p>
      <CloseIcon onClick={close} icon={faTimes} />
    </AlertStyled>
  );
}

export default Alert;
