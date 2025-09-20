import { ScrollArea, ScrollBar } from "@/components/ui/scroll-area";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { useMemo } from "react";
import { type OptionStraddle, straddleCompareFn } from "./option-chain-utils";

export function ExpiryOptions(props: {
  straddle: OptionStraddle;
}) {
  const rows = useMemo(
    () => Object.entries(props.straddle).sort(straddleCompareFn),
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
