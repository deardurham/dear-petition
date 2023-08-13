import { vi } from 'vitest';
import { getErrorList, hasValidationsErrors } from '../../util/errors';

const mockGetErrorList = {
  mockErrors: {
    errorOne: ['Error 1 message'],
    errorTwo: ['Error 2 message'],
  },
  getErrorList,
  hasValidationsErrors,
};

describe('Utils: errors.js', () => {
  afterEach(() => {
    vi.resetAllMocks();
  });

  it('hasValidationErrors returns true if errors exist', () => {
    const spy = vi.spyOn(mockGetErrorList, 'hasValidationsErrors');

    expect(spy.getMockName()).toEqual('hasValidationsErrors');
    expect(mockGetErrorList.hasValidationsErrors(mockGetErrorList.mockErrors)).toEqual(true);
    expect(spy).toHaveBeenCalledTimes(1);
  });

  it('hasValidationErrors returns false if no errors exist', () => {
    const spy = vi.spyOn(mockGetErrorList, 'hasValidationsErrors');

    expect(spy.getMockName()).toEqual('hasValidationsErrors');
    expect(mockGetErrorList.hasValidationsErrors({})).toEqual(false);
    expect(spy).toHaveBeenCalledTimes(1);
  });

  it('getErrorList returns a list of passed errors', () => {
    const spy = vi.spyOn(mockGetErrorList, 'getErrorList');
    expect(spy.getMockName()).toEqual('getErrorList');

    const errorList = [`ErrorOne: Error 1 message`, `ErrorTwo: Error 2 message`];
    expect(mockGetErrorList.getErrorList(mockGetErrorList.mockErrors)).toEqual(errorList);

    expect(spy).toHaveBeenCalledTimes(1);
  });

  it('getErrorList returns [] if no errors passed', () => {
    const getErrorListSpy = vi.fn(getErrorList);
    const noErrors = getErrorListSpy({});
    expect(noErrors).toStrictEqual([]);
    expect(getErrorListSpy).toHaveReturned();
  });
});
