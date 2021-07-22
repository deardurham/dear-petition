import axios from 'axios';
import { CSRF_COOKIE_NAME, CSRF_HEADER_KEY } from '../constants/authConstants';

const Axios = axios.create({
  baseURL: `/petition/api/`,
  timeout: 5000,
  withCredentials: true, // allow setting/passing cookies
  xsrfCookieName: CSRF_COOKIE_NAME,
  xsrfHeaderName: CSRF_HEADER_KEY,
});

export default Axios;

export const axiosBaseQuery =
  () =>
  async ({ url, method, data }) => {
    try {
      const result = await Axios({ url, method, data });
      console.log(result);
      return { data: result.data };
    } catch (axiosError) {
      console.log(axiosError);
      if (axiosError?.response?.status === 403) {
        // TODO
        Axios({ url: 'refresh/token/', method: 'post' }).then((refreshData) => {
          console.log(refreshData);
        });
        // handle403Response();
        console.log('403 ERROR');
      }
      return {
        error: { status: axiosError.response?.status, data: axiosError.response?.data },
      };
    }
  };
