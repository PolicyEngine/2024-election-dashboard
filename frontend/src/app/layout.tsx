import { PolicyEngineShell } from "@policyengine/ui-kit/layout";
import "@policyengine/ui-kit/styles.css";

import type { Metadata, Viewport } from 'next';
import './globals.css';
import PolicyEngineHeader from '@/components/PolicyEngineHeader';

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
        <PolicyEngineHeader />
        {children}
              </PolicyEngineShell>
      </body>
    </html>
  );
}
