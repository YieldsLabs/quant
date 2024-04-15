use crate::config::StopLossConfig;
use crate::deserialize::smooth_deserialize;
use base::prelude::*;
use stop_loss::*;

#[inline]
pub fn map_to_stoploss(config: StopLossConfig) -> Box<dyn StopLoss> {
    match config {
        StopLossConfig::Atr {
            smooth_type,
            period,
            factor,
        } => Box::new(AtrStopLoss::new(
            smooth_deserialize(smooth_type as usize),
            period,
            factor,
        )),
    }
}
