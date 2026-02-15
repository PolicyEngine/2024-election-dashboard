import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { MantineProvider, createTheme } from "@mantine/core";
import "@mantine/core/styles.css";
import App from "./App";
import { designTokens } from "./designTokens";

const theme = createTheme({
  fontFamily: designTokens.fonts.body,
  primaryColor: "teal",
  headings: { fontFamily: designTokens.fonts.body },
});

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <MantineProvider theme={theme}>
      <App />
    </MantineProvider>
  </StrictMode>,
);
