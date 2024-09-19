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
    max_leverage: float

    def __eq__(self, other) -> bool:
        if isinstance(other, Symbol):
            return self.name == other.name

        return False

    def __hash__(self) -> int:
        return hash(self.name)

    def __str__(self):
        return self.name

    def __repr__(self) -> str:
        return f"Symbol({self})"
