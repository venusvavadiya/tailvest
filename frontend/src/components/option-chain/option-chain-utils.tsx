import type { OptionData } from "@/client";

export type OptionStraddle = Record<
  number,
  {
    call?: OptionData;
    put?: OptionData;
  }
>;

export function toOptionStraddle(options: OptionData[]): OptionStraddle {
  const straddle: OptionStraddle = {};
  for (const option of options) {
    if (!straddle[option.strike]) {
      straddle[option.strike] = {};
    }

    if (option.kind === "call") {
      straddle[option.strike]!.call = option;
    } else if (option.kind === "put") {
      straddle[option.strike]!.put = option;
    }
  }
  return straddle;
}

export function straddleCompareFn(
  a: [string, { call?: OptionData; put?: OptionData }],
  b: [string, { call?: OptionData; put?: OptionData }],
) {
  return Number(a[0]) - Number(b[0]);
}
