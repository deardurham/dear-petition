/* BASE COLORS */
export const colorWhite = '#ffffff';
export const colorBlack = '#262626';

export const colorGrey = '#82908d'; // green/grey

export const colorGreen = '#89af5b';
export const colorRed = '#b04846';
export const colorBlue = '#4082c3';
export const colorYellow = '#d1d156';

/* COLORS */
export const colorPrimary = '#3d8f9d';
export const colorBackground = colorWhite;

export const colorFontPrimary = colorBlack;

export const colorSuccess = colorBlue;
export const colorCaution = colorRed;
export const colorWarning = colorYellow;

/**
 * greyScale
 * @param {number} degree - Number, 0 - 10. 0 being black 10 being white
 */
export function greyScale(degree) {
  return `hsl(0, 0%, ${degree * 10}%)`;
}
