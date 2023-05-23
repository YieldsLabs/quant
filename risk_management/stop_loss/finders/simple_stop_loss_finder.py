from risk_management.stop_loss.finders.abstract_stop_loss_finder import AbstractStopLoss


class SimpleStopLossFinder(AbstractStopLoss):
    NAME = 'SMPL'

    def __init__(self, stop_loss_pct=0.02):
        super().__init__()
        self.stop_loss_pct = stop_loss_pct

    def next(self, entry_price, ohlcv):
        return entry_price * (1.0 - self.stop_loss_pct), entry_price * (1.0 + self.stop_loss_pct)
