use crate::{OHLCVSeries, StopLossLevels, TradeAction, OHLCV};
use core::prelude::*;

pub trait Signal: Send + Sync {
    fn lookback(&self) -> usize;
    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>);
}

pub trait Filter: Send + Sync {
    fn lookback(&self) -> usize;
    fn confirm(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>);
}

pub trait Pulse: Send + Sync {
    fn lookback(&self) -> usize;
    fn assess(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>);
}

pub trait BaseLine: Send + Sync {
    fn lookback(&self) -> usize;
    fn filter(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>);
}

pub trait Exit: Send + Sync {
    fn lookback(&self) -> usize;
    fn evaluate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>);
}

pub trait StopLoss: Send + Sync {
    fn lookback(&self) -> usize;
    fn find(&self, data: &OHLCVSeries) -> (Series<f32>, Series<f32>);
}

pub trait Strategy {
    fn next(&mut self, ohlcv: OHLCV) -> TradeAction;
    fn stop_loss(&self) -> StopLossLevels;
}
