import * as Sentry from '@sentry/react';

// get sentry dsn from vite env variables, otherwise just use example dsn (e.g. for local development)
// TODO: look into using a different fallback dsn for testing purposes
const SENTRY_DSN = import.meta.env.VITE_SENTRY_DSN || 'https://examplePublicKey@o0.ingest.sentry.io/0';

Sentry.init({
  dsn: SENTRY_DSN,

  // defaultIntegrations and sampleRate are set to prevent error reporting for front-end,
  // since we are only using sentry for feedback widget; change these values if error reporting is desired
  defaultIntegrations: false,
  sampleRate: 0,

  integrations: [
    Sentry.feedbackIntegration({
      colorScheme: 'light',
    }),
  ],
});
