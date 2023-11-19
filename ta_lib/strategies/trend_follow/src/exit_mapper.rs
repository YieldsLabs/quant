use base::Exit;
use exit::*;
use serde::Deserialize;

#[derive(Deserialize)]
#[serde(tag = "type")]
pub enum ExitConfig {
    Dumb {},
    Pattern { period: f32 },
    HighLow { period: f32 },
}

pub fn map_to_exit(config: ExitConfig) -> Box<dyn Exit> {
    match config {
        ExitConfig::Dumb {} => Box::new(DumbExit {}),
        ExitConfig::Pattern { period } => Box::new(PatternExit::new(period)),
        ExitConfig::HighLow { period } => Box::new(HighLowExit::new(period)),
    }
}
