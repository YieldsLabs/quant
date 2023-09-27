from dataclasses import dataclass


@dataclass(frozen=True)
class Symbol:
    name: str
    taker_fee: float
    maker_fee: float
    min_position_size: float
    min_price_size: float
    position_precision: int
    price_precision: int

    @property
    def fee(self):
        return self.maker_fee + self.taker_fee

    def __str__(self):
        return self.name

    def __repr__(self) -> str:
        return f"Symbol({self.name})"
