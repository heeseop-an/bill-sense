import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "@mantine/core/styles.css";
import { createTheme, MantineProvider } from "@mantine/core";

const theme = createTheme({
  /** Put your mantine theme override here */
});

const root = ReactDOM.createRoot(
  document.getElementById("root") as HTMLElement
);
root.render(
  <MantineProvider theme={theme}>
    <React.StrictMode>
      <App />
    </React.StrictMode>
  </MantineProvider>
);
