use base::StopLoss;
use crate::ATRStopLoss;

pub enum StopLossConfig {
    ATR {
        period: usize,
        multi: f32,
    }
}

pub fn map_to_stoploss(config: StopLossConfig) -> Box<dyn StopLoss + Send + Sync> {
    match config {
        StopLossConfig::ATR { period, multi } => Box::new(ATRStopLoss::new(period, multi)),
        _ =>  Box::new(ATRStopLoss::new(14, 2.0))
    }
}