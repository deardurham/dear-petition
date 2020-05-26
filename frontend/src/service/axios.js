import axios from 'axios';
import { USER } from '../constants/authConstants';
import { CSRF_HEADER_KEY, CSRF_TOKEN_LS_KEY } from '../constants/authConstants';

const Axios = axios.create({
  baseURL: `/petition/api/`,
  timeout: 5000,
  withCredentials: true // allow setting/passing cookies
});

/**
 * A Request interceptor.
 * first callback intercepts successfully formed requests
 * second callback handles errors, so pass through
 */
Axios.interceptors.request.use(
  request => {
    const csrfToken = localStorage.getItem(CSRF_TOKEN_LS_KEY);
    if (csrfToken) request.headers[CSRF_HEADER_KEY] = csrfToken;
    return request;
  },
  error => Promise.reject(error)
);

/**
 * A Response interceptor.
 * first callback handles success, so pass through
 * second callback handles errors
 */
Axios.interceptors.response.use(
  success => success,
  error => {
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

function handle403Response(error) {
  console.warn('user is logged out!');
  localStorage.removeItem(USER);
  window.location = '/';
}

function addCsrfToRequestHeader(request, csrfToken) {
  request.headers[CSRF_HEADER_KEY] = csrfToken;
}
