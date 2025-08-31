import { createClient } from "./client/client";

export const apiClient = createClient({
  baseUrl: "/",
});
