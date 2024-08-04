use crate::{StopLossLevels, TradeAction};
use core::prelude::*;
use timeseries::prelude::*;

pub trait Signal: Send + Sync {
    fn lookback(&self) -> usize;
    fn trigger(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>);
}

pub trait Confirm: Send + Sync {
    fn lookback(&self) -> usize;
    fn filter(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>);
}

pub trait Pulse: Send + Sync {
    fn lookback(&self) -> usize;
    fn assess(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>);
}

pub trait BaseLine: Send + Sync {
    fn lookback(&self) -> usize;
    fn filter(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>);
    fn close(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>);
}

pub trait Exit: Send + Sync {
    fn lookback(&self) -> usize;
    fn close(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>);
}

pub trait StopLoss: Send + Sync {
    fn lookback(&self) -> usize;
    fn find(&self, data: &OHLCVSeries) -> (Series<f32>, Series<f32>);
}

pub trait Strategy {
    fn next(&mut self, bar: &OHLCV) -> TradeAction;
    fn stop_loss(&self, bar: &OHLCV) -> StopLossLevels;
}
