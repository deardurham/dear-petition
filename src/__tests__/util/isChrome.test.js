import * as jdsom from 'jsdom';

describe('isChrome test', () => {
  const { JSDOM, ResourceLoader } = jdsom;
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
