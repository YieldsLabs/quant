use crate::config::StopLossConfig;
use crate::deserialize::smooth_deserialize;
use base::prelude::*;
use stop_loss::*;

#[inline]
pub fn map_to_stoploss(config: StopLossConfig) -> Box<dyn StopLoss> {
    match config {
        StopLossConfig::Atr { period, factor } => Box::new(AtrStopLoss::new(period, factor)),
        StopLossConfig::Dch { period, factor } => Box::new(DchStopLoss::new(period, factor)),
    }
}
