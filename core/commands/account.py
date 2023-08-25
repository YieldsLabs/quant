from dataclasses import dataclass

from .base import Command


@dataclass(frozen=True)
class AccountUpdate(Command):
    amount: float | int