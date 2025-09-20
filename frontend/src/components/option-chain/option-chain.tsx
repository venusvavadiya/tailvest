import type { OptionData } from "@/client";
import { Tabs } from "@/components/ui/tabs";
import { useCallback, useMemo } from "react";
import { ExpiryOptions } from "./expiry-options";
import { ExpiryTabsList } from "./expiry-tabs-list";
import { toOptionStraddle } from "./option-chain-utils";

export function OptionChain(props: {
  expiries: string[];
  expiry: string;
  onExpiryChange: (expiry: string) => void;
  options: OptionData[];
}) {
  const optionsStraddle = useMemo(
    () => toOptionStraddle(props.options),
    [props.options],
  );

  const onExpiryChange = useCallback(
    (expiry: string) => {
      props.onExpiryChange(expiry);
    },
    [props.onExpiryChange],
  );

  return (
    <div className="flex flex-col gap-1 p-1 w-full h-full overflow-hidden">
      <div className="flex-shrink-0">
        <Tabs value={props.expiry} onValueChange={onExpiryChange}>
          <ExpiryTabsList expiries={props.expiries} />
        </Tabs>
      </div>

      <div className="flex-1 overflow-hidden">
        <ExpiryOptions straddle={optionsStraddle} />
      </div>
    </div>
  );
}
