use crate::TradeAction;
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

pub trait Strategy {
    fn next(&mut self, bar: &OHLCV) -> TradeAction;
}
