import type { OptionData } from "@/client";
import { ScrollArea, ScrollBar } from "@/components/ui/scroll-area";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { useCallback, useMemo } from "react";
import { type OptionStraddle, toOptionStraddle } from "./option-chain-utils";

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
          <ExpiryTabs expiries={props.expiries} />
        </Tabs>
      </div>

      <div className="flex-1 overflow-hidden">
        <ExpiryOptions straddle={optionsStraddle} />
      </div>
    </div>
  );
}

function ExpiryTabs(props: {
  expiries: string[];
}) {
  return (
    <ScrollArea className="w-full">
      <TabsList className="w-full overflow-x-auto">
        {props.expiries.map((expiry) => (
          <TabsTrigger
            key={expiry}
            value={expiry}
            className="hover:cursor-pointer"
          >
            {expiry}
          </TabsTrigger>
        ))}
      </TabsList>

      <ScrollBar orientation="horizontal" />
    </ScrollArea>
  );
}

function ExpiryOptions(props: {
  straddle: OptionStraddle;
}) {
  const rows = useMemo(
    () =>
      Object.entries(props.straddle).sort(
        (a, b) => Number(a[0]) - Number(b[0]),
      ),
    [props.straddle],
  );

  return (
    <ScrollArea className="h-full w-full">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead className="text-right bg-muted">Bid</TableHead>
            <TableHead className="text-right bg-muted">Ask</TableHead>
            <TableHead className="text-right bg-muted">OI</TableHead>
            <TableHead className="font-medium text-center bg-muted">
              Strike
            </TableHead>
            <TableHead className="text-right bg-muted">Bid</TableHead>
            <TableHead className="text-right bg-muted">Ask</TableHead>
            <TableHead className="text-right bg-muted">OI</TableHead>
          </TableRow>
        </TableHeader>

        <TableBody>
          {rows.map(([strike, { call, put }]) => (
            <TableRow key={strike}>
              <TableCell className="font-mono text-right">
                {call?.bid?.toFixed(2)}
              </TableCell>
              <TableCell className="font-mono text-right">
                {call?.ask?.toFixed(2)}
              </TableCell>
              <TableCell className="font-mono text-right">{call?.oi}</TableCell>
              <TableCell className="font-mono font-medium text-center bg-muted">
                {Number(strike).toFixed(2)}
              </TableCell>
              <TableCell className="font-mono text-right">
                {put?.bid?.toFixed(2)}
              </TableCell>
              <TableCell className="font-mono text-right">
                {put?.ask?.toFixed(2)}
              </TableCell>
              <TableCell className="font-mono text-right">{put?.oi}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>

      <ScrollBar orientation="vertical" />
      <ScrollBar orientation="horizontal" />
    </ScrollArea>
  );
}
