use crate::config::ExitConfig;
use crate::deserialize::{ma_deserialize, smooth_deserialize};
use base::prelude::*;
use exit::*;

#[inline]
pub fn map_to_exit(config: ExitConfig) -> Box<dyn Exit> {
    match config {
        ExitConfig::Ast { atr_period, factor } => Box::new(AstExit::new(atr_period, factor)),
        ExitConfig::Cci {
            smooth_type,
            period,
            factor,
            threshold,
        } => Box::new(CciExit::new(
            smooth_deserialize(smooth_type as usize),
            period,
            factor,
            threshold,
        )),
        ExitConfig::Dumb {} => Box::new(DumbExit {}),
        ExitConfig::HighLow { period } => Box::new(HighLowExit::new(period)),
        ExitConfig::Rsi {
            smooth_type,
            period,
            threshold,
        } => Box::new(RsiExit::new(
            smooth_deserialize(smooth_type as usize),
            period,
            threshold,
        )),
        ExitConfig::Trix {
            smooth_type,
            period,
            signal_period,
        } => Box::new(TrixExit::new(
            smooth_deserialize(smooth_type as usize),
            period,
            signal_period,
        )),
        ExitConfig::Mfi { period, threshold } => Box::new(MfiExit::new(period, threshold)),
        ExitConfig::Ma { ma, period } => Box::new(MaExit::new(ma_deserialize(ma as usize), period)),
    }
}
