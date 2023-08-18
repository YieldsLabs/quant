use crate::{OHLCVSeries, StopLossLevels, TradeAction, OHLCV};
use core::series::Series;

pub trait Signals {
    fn id(&self) -> String;
    fn entry(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>);
    fn exit(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>);
}

pub trait StopLoss {
    fn id(&self) -> String;
    fn next(&self, data: &OHLCVSeries) -> (Series<f32>, Series<f32>);
}

pub trait Strategy {
    fn id(&self) -> String;
    fn next(&mut self, ohlcv: OHLCV) -> TradeAction;
    fn stop_loss(&self) -> StopLossLevels;
}
