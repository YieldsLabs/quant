from core.actors import BaseActor


class ReefActor(BaseActor):
    def __init__(self):
        super().__init__()

    async def on_receive(self, msg: Any):
        print(msg)
