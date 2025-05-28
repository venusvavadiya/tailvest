from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Literal


@dataclass(frozen=True)
class Instrument:
    symbol: str


@dataclass(frozen=True)
class Equity(Instrument):
    pass


@dataclass(frozen=True)
class Index(Instrument):
    pass


@dataclass(frozen=True)
class Future(Instrument):
    underlying: Instrument
    expiry: date
    multiplier: int


OptionKind = Literal["call", "put"]

OptionStyle = Literal["american", "european"]


@dataclass(frozen=True)
class Option(Instrument):
    underlying: Instrument
    expiry: date
    strike: Decimal
    kind: OptionKind
    style: OptionStyle
    multiplier: int
