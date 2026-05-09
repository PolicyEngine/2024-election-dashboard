// Mantine v8 needs postcss-preset-mantine and postcss-simple-vars to compile
// its CSS. Tailwind v4 is layered on top via @tailwindcss/postcss so the
// PolicyEngine ui-kit theme tokens load through the same pipeline as the
// other PolicyEngine Next.js apps.
const config = {
  plugins: {
    'postcss-preset-mantine': {},
    'postcss-simple-vars': {
      variables: {
        'mantine-breakpoint-xs': '36em',
        'mantine-breakpoint-sm': '48em',
        'mantine-breakpoint-md': '62em',
        'mantine-breakpoint-lg': '75em',
        'mantine-breakpoint-xl': '88em',
      },
    },
    '@tailwindcss/postcss': {},
  },
};

export default config;
