import { createProxyMiddleware } from 'http-proxy-middleware';

// docker-compose will avoid using the fallback due to always having one of OVERRIDE_API_PROXY or API_PROXY set
const FALLBACK_PROXY = 'http://localhost:8000';

const PROXY_PATHS = ['/petition/api', '/admin/', '/static/admin', '/password_reset/', '/reset/'];

export const setupProxyPlugin = () => ({
  name: 'configure-server-proxy',
  configureServer() {
    createProxyMiddleware(PROXY_PATHS, {
      target: process.env.OVERRIDE_API_PROXY || process.env.API_PROXY || FALLBACK_PROXY,
      changeOrigin: true,
    });
  },
});
