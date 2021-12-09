import axios from 'axios';
import { loggedOut } from '../slices/auth';
import { CSRF_COOKIE_NAME, CSRF_HEADER_KEY } from '../constants/authConstants';

const Axios = axios.create({
  baseURL: `/petition/api/`,
  timeout: 5 * 1000,
  withCredentials: true, // allow setting/passing cookies
  xsrfCookieName: CSRF_COOKIE_NAME,
  xsrfHeaderName: CSRF_HEADER_KEY,
});

export default Axios;

export const axiosBaseQuery =
  () =>
  async ({ url, method, timeout, data }, api) => {
    try {
      const config = { url, method, data };
      if (timeout) {
        config.timeout = timeout;
      }
      const result = await Axios(config);
      return { data: result.data };
    } catch (axiosError) {
      const isLoginAttempt =
        url === 'token/' && method.localeCompare('post', 'en', { sensitivity: 'accent' }) === 0;
      if (axiosError?.response?.status !== 401 || isLoginAttempt) {
        return {
          error: { status: axiosError.response?.status, data: axiosError.response?.data },
        };
      }
    }

    // retry logic - use refresh token to get new access key and try again
    try {
      await Axios({ url: 'token/refresh/', method: 'post' });
      const result = await Axios({ url, method, data }); // retry
      return { data: result.data };
    } catch (axiosError) {
      api.dispatch(loggedOut());
      return {
        error: { status: axiosError.response?.status, data: axiosError.response?.data },
      };
    }
  };
