from dataclasses import dataclass

from .base import Command


@dataclass(frozen=True)
class UpdateAccountSize(Command):
    amount: float
