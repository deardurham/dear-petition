import styled from 'styled-components';
import FormInput from '../../elements/Input/FormInput';
// import { colorRed } from '../../../styles/colors';
// import { motion } from 'framer-motion';

// export const FormErrors = styled(motion.div)`
//   p {
//     color: ${colorRed};
//   }
//   margin-bottom: 1.5rem;
// `;

export const InputStyled = styled(FormInput)`
  margin: 2rem 0;
  input {
    padding: 0.9rem;
  }
`;

export const PasswordInputStyled = styled(InputStyled)`
  margin: 0;
`;
