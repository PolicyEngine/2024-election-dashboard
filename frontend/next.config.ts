import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  // Mantine and react-plotly.js ship CJS interop and rely on browser globals.
  // Transpiling them through Next's pipeline avoids ESM/CJS mismatch errors
  // during build.
  transpilePackages: ['@mantine/core', '@mantine/hooks'],
  // Pin the workspace root so Turbopack does not silently pick up a stray
  // lockfile from a parent directory during local development or CI.
  turbopack: {
    root: process.cwd(),
  },
};

export default nextConfig;
