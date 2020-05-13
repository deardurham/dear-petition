import styled from 'styled-components';
import { colorGreyLight } from '../../../styles/colors';

export const PetitionListItemStyled = styled.li`
    display: flex;
    margin: 0 0 2rem 0;
    cursor: pointer;
    &:hover {
        background: ${colorGreyLight};
    }
    margin: 0;
    padding: 2rem;
`;

export const PetitionCellStyled = styled.div`
    display: flex;
    width: 33.33%;
`
