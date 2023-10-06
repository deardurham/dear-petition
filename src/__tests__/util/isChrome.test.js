import { vi } from 'vitest';

describe('isChrome test', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    vi.resetAllMocks();
  });

  afterEach(() => {
    vi.stubGlobal('chrome', null);
    vi.stubGlobal('navigator', {
      userAgent: '',
      vendor: '',
    });
  });

  /*
  it('Mock Chrome userAgent, vendor in JSDOM', () => {
      userAgent: `Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36`,
      vendor: 'Google Inc.',
      chrome: true,

  it('Mock Mozilla userAgent, vendor in JSDOM', () => {
      userAgent: `Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0`,
      vendor: '',
      chrome: false,
  
  it('Mock iPhoneSafari userAgent, vendor in JSDOM', () => {
      userAgent: `Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Mobile/15E148 Safari/604.1`,
      vendor: 'Apple Computer, Inc.',
      chrome: false,
    });
  */

  it('browser is Chrome', async () => {
    vi.stubGlobal('chrome', true);
    vi.stubGlobal('navigator', {
      userAgent: `Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36`,
      vendor: 'Google Inc.',
    });

    const result = (await import('../../util/isChrome.js')).default;
    expect(result).toEqual(true);
  });

  it('browser is Mozilla', async () => {
    console.log('before new stubs');
    console.log('window.chrome: ', window.chrome);
    console.log('window.vendor: ', window.navigator.vendor);

    vi.stubGlobal('chrome', undefined);
    vi.stubGlobal('navigator', {
      userAgent: `Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0`,
      vendor: '',
    });

    console.log('after new stubs');
    console.log('window.chrome: ', window.chrome);
    console.log('window.vendor: ', window.navigator.vendor);

    const result = (await import('../../util/isChrome.js')).default;
    expect(result).toEqual(false);
  });
});
