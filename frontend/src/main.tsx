import "./custom.css";

import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { RouterProvider, createRouter } from "@tanstack/react-router";
import { ThemeProvider } from "next-themes";
import { StrictMode } from "react";
import reactDom from "react-dom/client";
import { routeTree } from "./routeTree.gen";

const router = createRouter({
  routeTree,
  pathParamsAllowedCharacters: ["@"],
});

declare module "@tanstack/react-router" {
  interface Register {
    router: typeof router;
  }
}

const rqc = new QueryClient();

// Render the app
const rootElement = document.getElementById("root")!;
if (!rootElement.innerHTML) {
  const root = reactDom.createRoot(rootElement);
  root.render(
    <StrictMode>
      <ThemeProvider attribute="class">
        <QueryClientProvider client={rqc}>
          <RouterProvider router={router} />
        </QueryClientProvider>
      </ThemeProvider>
    </StrictMode>,
  );
}
