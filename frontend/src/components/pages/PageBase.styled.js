import styled from "styled-components";
import { motion } from "framer-motion";

export const PageBaseStyled = styled(motion.main)`
    flex: 1;
    display: flex; 
    flex-direction: column;
`;

export const PageHeader = styled.header`
    padding: 4rem;
`;

export const PageLogo = styled.div`
    img {
        width: 260px;
    }
`;

export const PageContentWrapper = styled.section`
    flex: 1;
`;
