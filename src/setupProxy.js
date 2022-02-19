const { createProxyMiddleware } = require('http-proxy-middleware'); // eslint-disable-line import/no-extraneous-dependencies

// docker-compose will avoid using the fallback due to always having one of OVERRIDE_API_PROXY or API_PROXY set
const FALLBACK_PROXY = 'http://localhost:8000';

module.exports = (app) => {
  const proxyOptions = createProxyMiddleware({
    target: process.env.OVERRIDE_API_PROXY || process.env.API_PROXY || FALLBACK_PROXY,
    changeOrigin: true,
  });
  app.use('/petition/api', proxyOptions);
  app.use('/admin(-\\w+)?/', proxyOptions);
  app.use('/static/admin', proxyOptions);
  app.use('/password_reset/', proxyOptions);
  app.use('/reset/', proxyOptions);
};
