import * as jdsom from 'jsdom';

describe('isChrome test', () => {
  const { JSDOM, ResourceLoader } = jdsom;

  const setWindowProps = ({ userAgent, vendor, chrome }) => {
    const loader = new ResourceLoader({
      userAgent: userAgent,
    });
    const dom = new JSDOM(``, { resources: loader });
    dom.window.chrome = chrome;

    const isChromium = dom.window.chrome;
    const winNav = dom.window.navigator;
    // window.navigator.vendor is deprecated
    // https://developer.mozilla.org/en-US/docs/Web/API/Navigator/vendor
    // unable to set vendor on window object in JSDOM, readonly
    // const vendorName = winNav.vendor;
    const vendorName = vendor;
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

    return isChrome;
  };

  it('Mock Chrome userAgent, vendor in JSDOM', () => {
    const isChrome = setWindowProps({
      userAgent: 'Chrome/116.0.5845.187 (Official Build) <platform> (<platform-details>)',
      vendor: 'Google Inc.',
      chrome: true,
    });

    expect(isChrome).toBe(true);
  });

  it('Mock Mozilla userAgent, vendor in JSDOM', () => {
    const isChrome = setWindowProps({
      userAgent: 'Mozilla/5.0 (win32) AppleWebKit/537.36 (KHTML, like Gecko) jsdom/19.0.0',
      vendor: '',
      chrome: false,
    });

    expect(isChrome).toBe(false);
  });

  it('Mock iPhoneSafari userAgent, vendor in JSDOM', () => {
    const isChrome = setWindowProps({
      userAgent:
        'Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Mobile/15E148 Safari/604.1',
      vendor: 'Apple Computer, Inc.',
      chrome: false,
    });

    expect(isChrome).toBe(false);
  });
});
