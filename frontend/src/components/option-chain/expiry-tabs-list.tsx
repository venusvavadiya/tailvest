import { ScrollArea, ScrollBar } from "@/components/ui/scroll-area";
import { TabsList, TabsTrigger } from "@/components/ui/tabs";

export function ExpiryTabsList(props: {
  expiries: string[];
}) {
  return (
    <ScrollArea className="w-full">
      <TabsList className="w-full rounded-none overflow-x-auto">
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
