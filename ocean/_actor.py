from typing import Union

from core.actors import BaseActor
from core.queries.broker import GetSymbol, GetSymbols

OceanEvent = Union[GetSymbols, GetSymbol]


class OceanActor(BaseActor):
    def __init__(self):
        super().__init__()

    async def on_receive(self, _msg: OceanEvent):
        print(_msg)
