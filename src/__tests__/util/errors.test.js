import { vi } from 'vitest';
import { getErrorList, hasValidationsErrors } from '../../util/errors';

describe('Utils: errors.js', () => {
  afterEach(() => {
    vi.resetAllMocks();
  });

  it('hasValidationsErrors returns true if errors exist', () => {
    const hasValidationsErrorsSpy = vi.fn(hasValidationsErrors);
    const mockErrors = {
      errorOne: ['Error 1 message'],
      errorTwo: ['Error 2 message'],
    };
    const hasErrors = hasValidationsErrorsSpy(mockErrors);
    expect(hasErrors).toBe(true);
    expect(hasValidationsErrorsSpy).toHaveBeenCalledTimes(1);
    expect(hasValidationsErrorsSpy).toHaveReturned();
  });

  it('hasValidationsErrors returns false if no errors exist', () => {
    const hasValidationsErrorsSpy = vi.fn(hasValidationsErrors);
    const noErrors = hasValidationsErrorsSpy({});
    expect(noErrors).toBe(false);
    expect(hasValidationsErrorsSpy).toHaveBeenCalledTimes(1);
    expect(hasValidationsErrorsSpy).toHaveReturned();
  });

  it('getErrorList returns a list of passed errors', () => {
    const getErrorListSpy = vi.fn(getErrorList);
    const mockErrors = {
      errorOne: ['Error 1 message'],
      errorTwo: ['Error 2 message'],
    };
    const expectedResult = [`ErrorOne: Error 1 message`, `ErrorTwo: Error 2 message`];
    const result = getErrorListSpy(mockErrors);

    expect(result).toEqual(expectedResult);
    expect(getErrorListSpy).toHaveBeenCalledTimes(1);
    expect(getErrorListSpy).toHaveReturned();
  });

  it('getErrorList returns [] if no errors passed', () => {
    const getErrorListSpy = vi.fn(getErrorList);
    const noErrors = getErrorListSpy({});
    expect(noErrors).toStrictEqual([]);
    expect(getErrorListSpy).toHaveBeenCalledTimes(1);
    expect(getErrorListSpy).toHaveReturned();
  });
});
