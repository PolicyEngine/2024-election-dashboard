import { PolicyEngineShell } from "@policyengine/ui-kit/layout";
import "@policyengine/ui-kit/styles.css";

import type { Metadata, Viewport } from 'next';
import './globals.css';
import Script from 'next/script';
export const metadata: Metadata = {
  title: '2024 election household impact calculator | PolicyEngine',
  description:
    'Compare how tax proposals from the 2024 presidential candidates would affect your household net income.',
};

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <PolicyEngineShell country="us">
        {children}
              </PolicyEngineShell>
        {/* Google Analytics: policyengine.org's GA4 property; this app is served at policyengine.org/us/2024-election-calculator through a rewrite, where the main site's GA does not reach. */}
        {process.env.NODE_ENV === 'production' && (
          <>
            <Script
              src="https://www.googletagmanager.com/gtag/js?id=G-2YHG89FY0N"
              strategy="afterInteractive"
            />
            <Script id="google-analytics" strategy="afterInteractive">
              {`window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date());
gtag('config', 'G-2YHG89FY0N');`}
            </Script>
          </>
        )}
      </body>
    </html>
  );
}
