use crate::ma_mapper::map_to_ma;
use base::prelude::*;
use baseline::*;
use serde::Deserialize;

#[derive(Deserialize)]
#[serde(tag = "type")]
pub enum BaseLineConfig {
    Ma { ma: f32, period: f32 },
}

pub fn map_to_baseline(config: BaseLineConfig) -> Box<dyn BaseLine> {
    match config {
        BaseLineConfig::Ma { ma, period } => {
            Box::new(MABaseLine::new(map_to_ma(ma as usize), period))
        }
    }
}
