from dataclasses import dataclass

from strategy.exit.base import Exit, ExitType


@dataclass(frozen=True)
class DumbExit(Exit):
    type: ExitType = ExitType.Dumb
