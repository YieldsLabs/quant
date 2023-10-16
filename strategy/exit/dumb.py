from dataclasses import dataclass

from strategy.exit.base import BaseExit


@dataclass(frozen=True)
class DumbExit(BaseExit):
    pass
