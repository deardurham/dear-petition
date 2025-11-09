import * as Sentry from '@sentry/react';

const SENTRY_DSN = 'https://8b15bbb6bc864b3ebdc0369ffbdd02c0@o262794.ingest.us.sentry.io/1462682';

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
