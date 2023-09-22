use base::StopLoss;
use stop_loss::ATRStopLoss;

pub enum StopLossConfig {
    Atr { period: f32, multi: f32 },
}

pub fn map_to_stoploss(config: StopLossConfig) -> Box<dyn StopLoss> {
    match config {
        StopLossConfig::Atr { period, multi } => Box::new(ATRStopLoss::new(period, multi)),
    }
}
