use crate::smooth_mapper::map_to_smooth;
use base::prelude::*;
use exit::*;
use serde::Deserialize;

#[derive(Deserialize)]
#[serde(tag = "type")]
pub enum ExitConfig {
    Ast {
        atr_period: f32,
        factor: f32,
    },
    Cci {
        smooth_type: f32,
        period: f32,
        factor: f32,
        threshold: f32,
    },
    Dumb {},
    HighLow {
        period: f32,
    },
    Rsi {
        smooth_type: f32,
        period: f32,
        threshold: f32,
    },
    Mfi {
        period: f32,
        threshold: f32,
    },
    Trix {
        smooth_type: f32,
        period: f32,
        signal_period: f32,
    },
}

pub fn map_to_exit(config: ExitConfig) -> Box<dyn Exit> {
    match config {
        ExitConfig::Ast { atr_period, factor } => Box::new(AstExit::new(atr_period, factor)),
        ExitConfig::Cci {
            smooth_type,
            period,
            factor,
            threshold,
        } => Box::new(CCIExit::new(
            map_to_smooth(smooth_type as usize),
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
        } => Box::new(RSIExit::new(
            map_to_smooth(smooth_type as usize),
            period,
            threshold,
        )),
        ExitConfig::Trix {
            smooth_type,
            period,
            signal_period,
        } => Box::new(TRIXExit::new(
            map_to_smooth(smooth_type as usize),
            period,
            signal_period,
        )),
        ExitConfig::Mfi { period, threshold } => Box::new(MFIExit::new(period, threshold)),
    }
}
