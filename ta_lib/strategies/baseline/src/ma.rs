use base::prelude::*;
use core::prelude::*;
use shared::{ma_indicator, MovingAverageType};
use signal::{
    MACandleSignal, MACrossSignal, MAQuadrupleSignal, MASurpassSignal, MATestingGroundSignal,
};

const DEFAULT_ATR_LOOKBACK: usize = 14;
const DEFAULT_ATR_FACTOR: f32 = 1.236;
const ONE: f32 = 1.;

pub struct MABaseLine {
    ma: MovingAverageType,
    period: usize,
    signal: Vec<Box<dyn Signal>>,
}

impl MABaseLine {
    pub fn new(ma: MovingAverageType, period: f32) -> Self {
        Self {
            ma,
            period: period as usize,
            signal: vec![Box::new(MASurpassSignal::new(ma, period))],
        }
    }
}

impl BaseLine for MABaseLine {
    fn lookback(&self) -> usize {
        let mut m = std::cmp::max(DEFAULT_ATR_LOOKBACK, self.period);

        for signal in &self.signal {
            m = std::cmp::max(m, signal.lookback());
        }

        m
    }

    fn filter(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let ma = ma_indicator(&self.ma, data, self.period);
        let diff = &ma - ma.shift(1);

        let dist = (&ma - &data.close).abs();
        let atr = data.atr(DEFAULT_ATR_LOOKBACK, Smooth::SMMA) * DEFAULT_ATR_FACTOR;

        (
            diff.sgt(&ONE) & dist.slt(&atr),
            diff.slt(&ONE) & dist.slt(&atr),
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
