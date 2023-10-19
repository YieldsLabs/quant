use base::StopLoss;
use serde::Deserialize;
use stop_loss::ATRStopLoss;

#[derive(Deserialize)]
#[serde(tag = "type")]
pub enum StopLossConfig {
    Atr { period: f32, multi: f32 },
}

pub fn map_to_stoploss(config: StopLossConfig) -> Box<dyn StopLoss> {
    match config {
        StopLossConfig::Atr { period, multi } => Box::new(ATRStopLoss::new(period, multi)),
    }
}
