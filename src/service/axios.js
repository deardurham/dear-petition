import axios from 'axios';
import { loggedOut } from '../slices/auth';
import { CSRF_COOKIE_NAME, CSRF_HEADER_KEY } from '../constants/authConstants';

const Axios = axios.create({
  baseURL: `/petition/api/`,
  timeout: 20 * 1000,
  withCredentials: true, // allow setting/passing cookies
  xsrfCookieName: CSRF_COOKIE_NAME,
  xsrfHeaderName: CSRF_HEADER_KEY,
});

export default Axios;

export const axiosBaseQuery =
  (initialApi) =>
  async ({ url, method, timeout, data, params, responseType }, api) => {
    const currentApi = api ?? initialApi;
    if (!currentApi) {
      throw new Error('Must provide api instance');
    }
    const requestConfig = { url, method, data, params, responseType };
    if (timeout) {
      requestConfig.timeout = timeout;
    }
    try {
      const result = await Axios(requestConfig);
      return { data: result.data, meta: { request: requestConfig, response: result } };
    } catch (axiosError) {
      const isLoginAttempt = url === 'token/' && method.localeCompare('post', 'en', { sensitivity: 'base' }) === 0;
      if (axiosError?.response?.status !== 401 || isLoginAttempt) {
        return {
          error: { status: axiosError.response?.status, data: axiosError.response?.data },
        };
      }
    }

    // retry logic - use refresh token to get new access key and try again
    try {
      await Axios({ url: 'token/refresh/', method: 'post' });
      const result = await Axios(requestConfig); // retry
      return { data: result.data, meta: { request: requestConfig, response: result } };
    } catch (axiosError) {
      currentApi.dispatch(loggedOut());
      return {
        error: { status: axiosError.response?.status, data: axiosError.response?.data },
      };
    }
  };

export const manualAxiosRequest = async ({ url, method, timeout, data, params, responseType }) => {
  const store = (await import('../store')).default;
  const result = await axiosBaseQuery()({ url, method, timeout, data, params, responseType }, store);
  if ('error' in result) {
    throw result.error;
  }
  return result;
};
