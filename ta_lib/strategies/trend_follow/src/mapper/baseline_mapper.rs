use crate::config::BaseLineConfig;
use crate::deserialize::ma_deserialize;
use base::prelude::*;
use baseline::*;

#[inline]
pub fn map_to_baseline(config: BaseLineConfig) -> Box<dyn BaseLine> {
    match config {
        BaseLineConfig::Ma { ma, period } => {
            Box::new(MaBaseLine::new(ma_deserialize(ma as usize), period))
        }
    }
}
