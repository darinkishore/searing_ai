import App from './table/App.svelte';

import * as Sentry from "@sentry/svelte";
import { BrowserTracing } from "@sentry/tracing";

// Initialize the Sentry SDK here
Sentry.init({
  dsn: "https://8bcd2aa3a2bf415c81734eae21c23e20@o4503939342532608.ingest.sentry.io/4503939344039937",
  integrations: [new BrowserTracing()],

  // Set tracesSampleRate to 1.0 to capture 100%
  // of transactions for performance monitoring.
  // We recommend adjusting this value in production
  tracesSampleRate: 1.0,
});

window.htmx = require('htmx.org');

const app = new App({
	target: document.getElementById("svelte-table")
});

export default app;