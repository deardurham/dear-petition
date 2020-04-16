import { createGlobalStyle } from 'styled-components';
import normalize from './normalize';
import { colorFontPrimary, colorBlue } from './colors';
import { fontPrimary } from './fonts';

export default createGlobalStyle`
    ${normalize}

    :root {
        font-size: 10px;
    }

    ul, ol {
        margin: 0;
        padding: 0;
        list-style: none;
    }

    li {
        display: block;
    }

    a {
        color: ${colorBlue};
        text-decoration: none;
    }

    body {
        margin: 0;
        font-family: ${fontPrimary}
        font-size: 1.5rem;
        box-sizing: border-box;
    }

    h1 {
        color: ${colorFontPrimary};
        font-size: 3rem;
        font-weight: normal;
    }

    h2 {
        color: ${colorFontPrimary};
        font-size: 2.5rem;
        font-weight: normal;
    }

    h3 {
        color: ${colorFontPrimary};
        font-size: 2rem;
        font-weight: normal;
    }

    h4 {
        color: ${colorFontPrimary};
        font-size: 1.5rem;
    }

    h5 {
        color: ${colorFontPrimary};
        font-size: 1.5rem;
        font-weight: bold;
    }

    p {
        color: ${colorFontPrimary};
        font-size: 1.5rem;
    }
`;
