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

  it('browser is Chrome, isChrome=true', async () => {
    vi.stubGlobal('chrome', true);
    vi.stubGlobal('navigator', {
      userAgent: `Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36`,
      vendor: 'Google Inc.',
    });

    const result = (await import('../../util/isChrome.js')).default;
    expect(result).toEqual(true);
  });

  it('browser is Mozilla, isChrome=false', async () => {
    vi.stubGlobal('chrome', undefined);
    vi.stubGlobal('navigator', {
      userAgent: `Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0`,
      vendor: '',
    });

    const result = (await import('../../util/isChrome.js')).default;
    expect(result).toEqual(false);
  });
});
