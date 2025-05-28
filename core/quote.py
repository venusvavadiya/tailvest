from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from core.instrument import Instrument


@dataclass(frozen=True)
class Bid:
    price: Decimal
    size: int


@dataclass(frozen=True)
class Ask:
    price: Decimal
    size: int


@dataclass(frozen=True)
class Quote:
    instrument: Instrument
    timestamp: datetime
    bid: Bid
    ask: Ask
