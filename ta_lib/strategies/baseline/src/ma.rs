use base::prelude::*;
use core::prelude::*;
use indicator::{ma_indicator, MovingAverageType};
use signal::{MaCrossSignal, MaQuadrupleSignal, MaSurpassSignal, MaTestingGroundSignal};

const DEFAULT_ATR_LOOKBACK: usize = 14;
const DEFAULT_ATR_FACTOR: f32 = 1.236;

pub struct MaBaseLine {
    ma: MovingAverageType,
    period: usize,
    signal: Vec<Box<dyn Signal>>,
}

impl MaBaseLine {
    pub fn new(ma: MovingAverageType, period: f32) -> Self {
        Self {
            ma,
            period: period as usize,
            signal: vec![
                Box::new(MaSurpassSignal::new(ma, period)),
                // Box::new(MaQuadrupleSignal::new(ma, period)),
            ],
        }
    }
}

impl BaseLine for MaBaseLine {
    fn lookback(&self) -> usize {
        let mut m = std::cmp::max(DEFAULT_ATR_LOOKBACK, self.period);

        for signal in &self.signal {
            m = std::cmp::max(m, signal.lookback());
        }

        m
    }

    fn filter(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let ma = ma_indicator(&self.ma, data, self.period);
        let prev_ma = ma.shift(1);

        let dist = (&ma - &data.close).abs();
        let atr = data.atr(DEFAULT_ATR_LOOKBACK, Smooth::SMMA) * DEFAULT_ATR_FACTOR;

        (
            ma.sgt(&prev_ma) & dist.slt(&atr),
            ma.slt(&prev_ma) & dist.slt(&atr),
        )
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let lookback = self.lookback();

        let mut go_long_signal: Series<bool> = Series::zero(lookback).into();
        let mut go_short_signal: Series<bool> = Series::zero(lookback).into();

        for signal in &self.signal {
            let (go_long, go_short) = signal.generate(data);

            go_long_signal = go_long_signal | go_long;
            go_short_signal = go_short_signal | go_short;
        }

        (go_long_signal, go_short_signal)
    }
}
