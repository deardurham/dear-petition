import * as jdsom from 'jsdom';

describe('isChrome test', () => {
  const { JSDOM, ResourceLoader } = jdsom;

  const setWindowProps = ({ userAgent, vendor }) => {
    const loader = new ResourceLoader({
      userAgent: userAgent,
    });
    const dom = new JSDOM(``, { resources: loader });
    dom.window.chrome = true;

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
    });

    expect(isChrome).toBe(true);
  });

  it('Mock Mozilla userAgent, vendor in JSDOM', () => {
    const isChrome = setWindowProps({
      userAgent: 'Mozilla/5.0 (win32) AppleWebKit/537.36 (KHTML, like Gecko) jsdom/19.0.0',
      vendor: '',
    });

    expect(isChrome).toBe(false);
  });

  it('userAgent includes Chrome, returns true', () => {
    const loader = new ResourceLoader({
      userAgent: 'Chrome/116.0.5845.187 (Official Build) <platform> (<platform-details>)',
    });

    const dom = new JSDOM(``, { resources: loader });
    const userAgent = dom.window.navigator.userAgent;

    const includesChrome = userAgent.search(/\bchrome\b/i) > -1;

    expect(includesChrome).toBe(true);
  });

  it('userAgent Mozilla returns false', () => {
    const loader = new ResourceLoader({
      userAgent: 'Mozilla/5.0 (win32) AppleWebKit/537.36 (KHTML, like Gecko) jsdom/19.0.0',
    });
    const dom = new JSDOM(``, { resources: loader });
    const userAgent = dom.window.navigator.userAgent;

    const includesChrome = userAgent.search(/\bchrome\b/i) > -1;

    expect(includesChrome).toBe(false);
  });
});
