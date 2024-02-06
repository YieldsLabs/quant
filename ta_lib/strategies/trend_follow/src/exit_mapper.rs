use crate::ma_mapper::map_to_ma;
use crate::smooth_mapper::map_to_smooth;
use base::prelude::*;
use exit::*;
use serde::Deserialize;

#[derive(Deserialize)]
#[serde(tag = "type")]
pub enum ExitConfig {
    Ast {
        atr_period: f32,
        multi: f32,
    },
    Dumb {},
    Pattern {
        period: f32,
    },
    HighLow {
        period: f32,
    },
    Ma {
        ma: f32,
        period: f32,
    },
    Rsi {
        smooth_type: f32,
        period: f32,
        threshold: f32,
    },
    Ce {
        period: f32,
        atr_period: f32,
        multi: f32,
    },
}

pub fn map_to_exit(config: ExitConfig) -> Box<dyn Exit> {
    match config {
        ExitConfig::Ast { atr_period, multi } => Box::new(AstExit::new(atr_period, multi)),
        ExitConfig::Ce {
            period,
            atr_period,
            multi,
        } => Box::new(CeExit::new(period, atr_period, multi)),
        ExitConfig::Dumb {} => Box::new(DumbExit {}),
        ExitConfig::Pattern { period } => Box::new(PatternExit::new(period)),
        ExitConfig::HighLow { period } => Box::new(HighLowExit::new(period)),
        ExitConfig::Ma { ma, period } => Box::new(MAExit::new(map_to_ma(ma as usize), period)),
        ExitConfig::Rsi {
            smooth_type,
            period,
            threshold,
        } => Box::new(RSIExit::new(
            map_to_smooth(smooth_type as usize),
            period,
            threshold,
        )),
    }
}
