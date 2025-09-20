import { apiClient } from "@/api-client";
import { getOptions } from "@/client";
import { OptionChain } from "@/components/option-chain/option-chain";
import { Separator } from "@/components/ui/separator";
import { useQuery } from "@tanstack/react-query";
import { createFileRoute } from "@tanstack/react-router";
import { useCallback } from "react";

export const Route = createFileRoute("/tickers/$ticker/options")({
  component: RouteComponent,
  validateSearch: (search: { expiry?: string }) => search,
});

function RouteComponent() {
  const params = Route.useParams();
  const search = Route.useSearch();
  const navigate = Route.useNavigate();

  const expiriesQuery = useQuery({
    queryKey: ["expiries", params.ticker, search.expiry],
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

  const onExpiryChange = useCallback(
    (expiry: string) => {
      navigate({ search: { expiry } });
    },
    [navigate],
  );

  if (expiriesQuery.isLoading) {
    return <div>Loading...</div>;
  }

  if (expiriesQuery.isError) {
    return <div>Error: {expiriesQuery.error.message}</div>;
  }

  if (!expiriesQuery.data?.data) {
    return <div>No data</div>;
  }

  const expiriesData = expiriesQuery.data.data;

  return (
    <div className="flex w-screen h-screen overflow-hidden">
      <div className="w-1/2 overflow-hidden">
        <h2 className="text-xl font-bold px-2 py-1">{params.ticker}</h2>

        <Separator orientation="horizontal" className="w-full" />

        <OptionChain
          expiries={expiriesData.expiries}
          expiry={expiriesData.expiry}
          options={expiriesData.options}
          onExpiryChange={onExpiryChange}
        />
      </div>

      <Separator orientation="vertical" className="h-screen" />

      <div className="w-1/2 overflow-hidden">
        <h2 className="text-xl font-bold px-2 py-1">Strategy Builder</h2>

        <Separator orientation="horizontal" className="w-full" />
      </div>
    </div>
  );
}
