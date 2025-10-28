import * as Sentry from '@sentry/react';

// get sentry dsn from vite env variables, otherwise just use example dsn (e.g. for local development)
// TODO: look into using a different fallback dsn for testing purposes
const SENTRY_DSN = import.meta.env.VITE_SENTRY_DSN || 'https://examplePublicKey@o0.ingest.sentry.io/0';

Sentry.init({
  dsn: SENTRY_DSN,

  integrations: [
    Sentry.feedbackIntegration({
      // Additional SDK configuration goes in here, for example:
      colorScheme: 'light',
    }),
  ],
});
