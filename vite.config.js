/// <reference types="vitest" />
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import eslint from 'vite-plugin-eslint';
import http from 'http';

// docker-compose will avoid using the fallback due to always having one of OVERRIDE_API_PROXY or API_PROXY set
const FALLBACK_PROXY = 'http://127.0.0.1:8000';
const TARGET = process.env.OVERRIDE_API_PROXY || process.env.API_PROXY || FALLBACK_PROXY;

const agent = new http.Agent();

const PROXIES = {};
const PROXY_PATHS = ['/petition/api', '/admin/', '/static/admin', '/password_reset/', '/reset/', '/portal/'];
PROXY_PATHS.forEach((path) => {
  PROXIES[path] = { target: TARGET, changeOrigin: true, secure: false, agent };
});

export default defineConfig(() => ({
  build: {
    outDir: 'build',
    assetsDir: 'static',
  },
  server: {
    host: '0.0.0.0',
    port: 3000,
    proxy: PROXIES,
  },
  assetsInclude: '**/*.md',
  plugins: [react(), eslint()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: 'src/setupTests.js',
    testTimeout: 30000,
  },
}));
