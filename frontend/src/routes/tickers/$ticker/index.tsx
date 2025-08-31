import { apiClient } from "@/api-client";
import { getExpiries } from "@/client";
import { useQuery } from "@tanstack/react-query";
import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/tickers/$ticker/")({
  component: RouteComponent,
});

function RouteComponent() {
  const params = Route.useParams();

  const expiriesQuery = useQuery({
    queryKey: ["expiries", params.ticker],
    queryFn: () =>
      getExpiries({
        client: apiClient,
        path: {
          ticker: params.ticker,
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
