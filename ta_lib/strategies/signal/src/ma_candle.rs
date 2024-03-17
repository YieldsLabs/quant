use base::prelude::*;
use candlestick::{hexad, master_candle, slingshot, three_candles, three_one_two};
use core::prelude::*;
use shared::{ma_indicator, MovingAverageType};

pub struct MACandleSignal {
    ma: MovingAverageType,
    period: usize,
}

impl MACandleSignal {
    pub fn new(ma: MovingAverageType, period: f32) -> Self {
        Self {
            ma,
            period: period as usize,
        }
    }
}

impl Signal for MACandleSignal {
    fn lookback(&self) -> usize {
        self.period
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let ma = ma_indicator(&self.ma, data, self.period);

        (
            (slingshot::bullish(&data.open, &data.high, &data.low, &data.close)
                | master_candle::bullish(&data.open, &data.high, &data.low, &data.close)
                | three_candles::bullish(&data.open, &data.close)
                | hexad::bullish(&data.open, &data.high, &data.close)
                | three_one_two::bullish(&data.open, &data.high, &data.low, &data.close))
                & data.close.sgt(&ma),
            (slingshot::bearish(&data.open, &data.high, &data.low, &data.close)
                | master_candle::bearish(&data.open, &data.high, &data.low, &data.close)
                | three_candles::bearish(&data.open, &data.close)
                | hexad::bearish(&data.open, &data.low, &data.close)
                | three_one_two::bearish(&data.open, &data.high, &data.low, &data.close))
                & data.close.slt(&ma),
        )
    }
}
