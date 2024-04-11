use base::prelude::*;
use core::prelude::*;
use trend::qstick;

pub struct QSTICKFlipSignal {
    smooth_type: Smooth,
    period: usize,
}

impl QSTICKFlipSignal {
    pub fn new(smooth_type: Smooth, period: f32) -> Self {
        Self {
            smooth_type,
            period: period as usize,
        }
    }
}

impl Signal for QSTICKFlipSignal {
    fn lookback(&self) -> usize {
        self.period
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let qstick = qstick(&data.open, &data.close, self.smooth_type, self.period);

        (
            qstick.cross_over(&ZERO_LINE),
            qstick.cross_under(&ZERO_LINE),
        )
    }
}
