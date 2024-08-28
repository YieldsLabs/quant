use crate::{StopLossLevels, TradeAction};
use core::prelude::*;
use timeseries::prelude::*;

pub trait Signal: Send + Sync {
    fn lookback(&self) -> usize;
    fn trigger(&self, data: &OHLCVSeries) -> (Rule, Rule);
}

pub trait Confirm: Send + Sync {
    fn lookback(&self) -> usize;
    fn filter(&self, data: &OHLCVSeries) -> (Rule, Rule);
}

pub trait Pulse: Send + Sync {
    fn lookback(&self) -> usize;
    fn assess(&self, data: &OHLCVSeries) -> (Rule, Rule);
}

pub trait BaseLine: Send + Sync {
    fn lookback(&self) -> usize;
    fn filter(&self, data: &OHLCVSeries) -> (Rule, Rule);
    fn close(&self, data: &OHLCVSeries) -> (Rule, Rule);
}

pub trait Exit: Send + Sync {
    fn lookback(&self) -> usize;
    fn close(&self, data: &OHLCVSeries) -> (Rule, Rule);
}

pub trait StopLoss: Send + Sync {
    fn lookback(&self) -> usize;
    fn find(&self, data: &OHLCVSeries) -> (Price, Price);
}

pub trait Strategy {
    fn next(&mut self, bar: &OHLCV) -> TradeAction;
    fn stop_loss(&self, bar: &OHLCV) -> StopLossLevels;
}
