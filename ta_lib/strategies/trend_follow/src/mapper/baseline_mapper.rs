use crate::config::BaseLineConfig;
use crate::deserialize::{ma_deserialize, source_deserialize};
use base::prelude::*;
use baseline::*;

#[inline]
pub fn map_to_baseline(config: BaseLineConfig) -> Box<dyn BaseLine> {
    match config {
        BaseLineConfig::Ma { source, ma, period } => Box::new(MaBaseLine::new(
            source_deserialize(source as usize),
            ma_deserialize(ma as usize),
            period,
        )),
    }
}
