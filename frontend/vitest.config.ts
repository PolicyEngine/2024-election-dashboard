import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import path from 'node:path';

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./src/test/setup.ts'],
    server: {
      deps: {
        // Mantine and the PolicyEngine ui-kit ship ESM that Vitest needs to
        // process inline so jsdom + jest-dom can render their components.
        inline: ['@policyengine/ui-kit', '@mantine/core', '@mantine/hooks'],
      },
    },
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
});
