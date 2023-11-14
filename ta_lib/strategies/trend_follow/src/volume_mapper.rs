use base::Volume;
use serde::Deserialize;
use volume_filter::*;

#[derive(Deserialize)]
#[serde(tag = "type")]
pub enum VolumeConfig {
    Dumb {},
}

pub fn map_to_volume(config: VolumeConfig) -> Box<dyn Volume> {
    match config {
        VolumeConfig::Dumb {} => Box::new(DumbVolume {}),
    }
}
