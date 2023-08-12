import { vi } from 'vitest';
import { getErrorList, hasValidationsErrors } from '../util/errors';

const mockGetErrorList = {
  mockErrors: {
    errorOne: ['Error 1 message'],
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

  it('getErrorList should return a list of passed errors', () => {
    const spy = vi.spyOn(mockGetErrorList, 'getErrorList');
    expect(spy.getMockName()).toEqual('getErrorList');

    expect(mockGetErrorList.getErrorList(mockGetErrorList.mockErrors)).toEqual([`ErrorOne: Error 1 message`]);

    expect(spy).toHaveBeenCalledTimes(1);
  });

  //   it('should return [] if no errors passed', () => {
  //     const spy = vi.spyOn(mockGetErrorList, 'getErrorList');
  //     expect(spy.getMockName()).toEqual('getErrorList');

  //     const mockValidationObj = Object.entries({});
  //     expect(mockGetErrorList.getErrorList(mockValidationObj)).toEqual([]);

  //     expect(spy).toHaveBeenCalledTimes(1);
  //   });
});
