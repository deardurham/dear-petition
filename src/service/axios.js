import axios from 'axios';
import { loggedOut } from '../slices/auth';
import { CSRF_COOKIE_NAME, CSRF_HEADER_KEY } from '../constants/authConstants';

const Axios = axios.create({
  baseURL: `/petition/api/`,
  timeout: 25 * 1000,
  withCredentials: true, // allow setting/passing cookies
  xsrfCookieName: CSRF_COOKIE_NAME,
  xsrfHeaderName: CSRF_HEADER_KEY,
});

export default Axios;

export const axiosBaseQuery =
  () =>
  async ({ url, method, data }, api) => {
    try {
      const result = await Axios({ url, method, data });
      return { data: result.data };
    } catch (axiosError) {
      if (axiosError?.response?.status !== 403) {
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
