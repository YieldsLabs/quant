use crate::{OHLCVSeries, StopLossLevels, TradeAction, OHLCV};
use core::Series;

pub trait Signal: Send + Sync {
    fn lookback(&self) -> usize;
    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>);
}

pub trait Exit: Send + Sync {
    fn lookback(&self) -> usize;
    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>);
}

pub trait StopLoss: Send + Sync {
    fn lookback(&self) -> usize;
    fn next(&self, data: &OHLCVSeries) -> (Series<f32>, Series<f32>);
}

pub trait Filter: Send + Sync {
    fn lookback(&self) -> usize;
    fn apply(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>);
}

pub trait Strategy {
    fn next(&mut self, ohlcv: OHLCV) -> TradeAction;
    fn stop_loss(&self) -> StopLossLevels;
}
