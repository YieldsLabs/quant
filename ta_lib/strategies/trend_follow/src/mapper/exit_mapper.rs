use crate::config::ExitConfig;
use crate::deserialize::{ma_deserialize, smooth_deserialize, source_deserialize};
use base::prelude::*;
use exit::*;

#[inline]
pub fn map_to_exit(config: ExitConfig) -> Box<dyn Exit> {
    match config {
        ExitConfig::Ast {
            source_type,
            atr_period,
            factor,
        } => Box::new(AstExit::new(
            source_deserialize(source_type as usize),
            atr_period,
            factor,
        )),
        ExitConfig::Cci {
            source_type,
            smooth_type,
            period,
            factor,
            threshold,
        } => Box::new(CciExit::new(
            source_deserialize(source_type as usize),
            smooth_deserialize(smooth_type as usize),
            period,
            factor,
            threshold,
        )),
        ExitConfig::Dumb {} => Box::new(DumbExit {}),
        ExitConfig::HighLow { period } => Box::new(HighLowExit::new(period)),
        ExitConfig::Rsi {
            source_type,
            smooth_type,
            period,
            threshold,
        } => Box::new(RsiExit::new(
            source_deserialize(source_type as usize),
            smooth_deserialize(smooth_type as usize),
            period,
            threshold,
        )),
        ExitConfig::Trix {
            source_type,
            smooth_type,
            period,
            signal_period,
        } => Box::new(TrixExit::new(
            source_deserialize(source_type as usize),
            smooth_deserialize(smooth_type as usize),
            period,
            signal_period,
        )),
        ExitConfig::Mfi {
            source_type,
            period,
            threshold,
        } => Box::new(MfiExit::new(
            source_deserialize(source_type as usize),
            period,
            threshold,
        )),
        ExitConfig::Ma {
            source_type,
            ma,
            period,
        } => Box::new(MaExit::new(
            source_deserialize(source_type as usize),
            ma_deserialize(ma as usize),
            period,
        )),
    }
}
