from dataclasses import dataclass

from strategy.exit.base import BaseExit, ExitType


@dataclass(frozen=True)
class DumbExit(BaseExit):
    type: ExitType = ExitType.Dumb
