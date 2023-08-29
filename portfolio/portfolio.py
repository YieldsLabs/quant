from core.interfaces.abstract_event_manager import AbstractEventManager


class Portfolio(AbstractEventManager):
    def __init__(self):
        super().__init__()

    def handle_open_position(self):
        pass

    def handle_close_positon(self):
        pass

    def top_strategy(self):
        pass

    def open_positions(self):
        pass

    def equity(self):
        pass

    def drawdown(self):
        pass

    def total_pnl(self):
        pass