import { apiClient } from "@/api-client";
import { getOptions } from "@/client";
import { useQuery } from "@tanstack/react-query";
import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/tickers/$ticker/options")({
  component: RouteComponent,
  validateSearch: (search: { expiry?: string }) => search,
});

function RouteComponent() {
  const params = Route.useParams();
  const search = Route.useSearch();

  const expiriesQuery = useQuery({
    queryKey: ["expiries", params.ticker],
    queryFn: () =>
      getOptions({
        client: apiClient,
        path: {
          ticker: params.ticker,
        },
        query: {
          expiry: search.expiry,
        },
      }),
  });

  if (expiriesQuery.isLoading) {
    return <div>Loading...</div>;
  }

  if (expiriesQuery.isError) {
    return <div>Error: {expiriesQuery.error.message}</div>;
  }

  return <div>{JSON.stringify(expiriesQuery.data)}</div>;
}
