import { apiClient } from "@/api-client";
import { getExpiry } from "@/client";
import { useQuery } from "@tanstack/react-query";
import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/tickers/$ticker/expiries/$expiry/")({
  component: RouteComponent,
});

function RouteComponent() {
  const params = Route.useParams();

  const expiryQuery = useQuery({
    queryKey: ["expiry", params.expiry],
    queryFn: () =>
      getExpiry({
        client: apiClient,
        path: {
          ticker: params.ticker,
          expiry: params.expiry,
        },
      }),
  });

  if (expiryQuery.isLoading) {
    return <div>Loading...</div>;
  }

  if (expiryQuery.isError) {
    return <div>Error: {expiryQuery.error.message}</div>;
  }

  return <div>{JSON.stringify(expiryQuery.data)}</div>;
}
