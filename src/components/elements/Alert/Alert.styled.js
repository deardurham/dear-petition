import styled from 'styled-components';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { colorWarning, colorCaution, colorSuccess } from '../../../styles/colors';

export const AlertStyled = styled.div``;

export const IconStyled = styled(FontAwesomeIcon)`
  color: ${props => {
    switch (props.type) {
      case 'info':
        return colorWarning;
      case 'error':
        return colorCaution;
      case 'success':
        return colorSuccess;
      default:
        return colorSuccess;
    }
  }};
`;

export const CloseIcon = styled(FontAwesomeIcon)``;
