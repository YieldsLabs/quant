use base::Volume;
use serde::Deserialize;
use volume_filter::*;

#[derive(Deserialize)]
#[serde(tag = "type")]
pub enum VolumeConfig {
    Dumb { period: f32 },
    Osc { short_period: f32, long_period: f32 },
}

pub fn map_to_volume(config: VolumeConfig) -> Box<dyn Volume> {
    match config {
        VolumeConfig::Dumb { period } => Box::new(DumbVolume::new(period)),
        VolumeConfig::Osc {
            short_period,
            long_period,
        } => Box::new(OSCVolume::new(short_period, long_period)),
    }
}
