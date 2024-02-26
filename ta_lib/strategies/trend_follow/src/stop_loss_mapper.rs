use crate::smooth_mapper::map_to_smooth;
use base::prelude::*;
use serde::Deserialize;
use stop_loss::ATRStopLoss;

#[derive(Deserialize)]
#[serde(tag = "type")]
pub enum StopLossConfig {
    Atr {
        smooth_type: f32,
        period: f32,
        factor: f32,
    },
}

pub fn map_to_stoploss(config: StopLossConfig) -> Box<dyn StopLoss> {
    match config {
        StopLossConfig::Atr {
            smooth_type,
            period,
            factor,
        } => Box::new(ATRStopLoss::new(
            map_to_smooth(smooth_type as usize),
            period,
            factor,
        )),
    }
}
