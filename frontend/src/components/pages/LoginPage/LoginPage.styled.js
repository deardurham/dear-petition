import styled from 'styled-components';
import { motion } from 'framer-motion';

export const LoginPageStyled = styled(motion.div)`
    display: flex;
    flex-direction: column;
    align-items: center;
`;

export const LoginSplash = styled.div`
    margin-top: 20vh;
    max-width: 1000px;
    padding: 1rem;
`;

export const SplashLogo = styled.img`
    width: 100%;
    height: auto;
`;

export const LoginSection = styled.div`
    margin-top: 10vh;
    flex: 1;
`;
