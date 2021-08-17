// Source: https://stackoverflow.com/a/13348618
const isChromium = window.chrome;
const winNav = window.navigator;
const vendorName = winNav.vendor;
const isOpera = typeof window.opr !== 'undefined';
const isIEedge = winNav.userAgent.indexOf('Edge') > -1;
const isIOSChrome = winNav.userAgent.match('CriOS');

const isChrome =
  !isIOSChrome &&
  isChromium !== null &&
  typeof isChromium !== 'undefined' &&
  vendorName === 'Google Inc.' &&
  isOpera === false &&
  isIEedge === false;

export default isChrome;
