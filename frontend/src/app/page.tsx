'use client';

import { MantineProvider, createTheme } from '@mantine/core';
import App from '@/App';
import { designTokens } from '@/designTokens';

const theme = createTheme({
  fontFamily: designTokens.fonts.body,
  primaryColor: 'teal',
  headings: { fontFamily: designTokens.fonts.body },
});

export default function HomePage() {
  return (
    <MantineProvider theme={theme}>
      <App />
    </MantineProvider>
  );
}
