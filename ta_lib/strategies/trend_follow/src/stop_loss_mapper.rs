use base::prelude::*;
use serde::Deserialize;
use stop_loss::ATRStopLoss;

#[derive(Deserialize)]
#[serde(tag = "type")]
pub enum StopLossConfig {
    Atr { period: f32, factor: f32 },
}

pub fn map_to_stoploss(config: StopLossConfig) -> Box<dyn StopLoss> {
    match config {
        StopLossConfig::Atr { period, factor } => Box::new(ATRStopLoss::new(period, factor)),
    }
}
