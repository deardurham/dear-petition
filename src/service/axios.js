import axios from 'axios';
import { CSRF_COOKIE_NAME, CSRF_HEADER_KEY, USER } from '../constants/authConstants';

const Axios = axios.create({
  baseURL: `/petition/api/`,
  timeout: 5000,
  withCredentials: true, // allow setting/passing cookies
  xsrfCookieName: CSRF_COOKIE_NAME,
  xsrfHeaderName: CSRF_HEADER_KEY,
});

/**
 * A Response interceptor.
 * first callback handles success, so pass through
 * second callback handles errors
 */
Axios.interceptors.response.use(
  (success) => success,
  (error) => {
    if (error?.response) {
      const { status } = error.response;
      // Only care about 403s so far, so pass through
      if (status !== 403) return Promise.reject(error);
      return handle403Response(error);
    }
    return Promise.reject(error);
  }
);

export default Axios;

function handle403Response() {
  localStorage.removeItem(USER);
  window.location = '/';
}
