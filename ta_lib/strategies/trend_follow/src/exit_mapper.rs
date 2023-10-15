use base::Exit;
use exit::DumbExit;
use serde::Deserialize;

#[derive(Deserialize)]
#[serde(tag = "type", rename_all = "PascalCase")]
pub enum ExitConfig {
    Dumb {},
}

pub fn map_to_exit(config: ExitConfig) -> Box<dyn Exit> {
    match config {
        ExitConfig::Dumb {} => Box::new(DumbExit {}),
        _ => Box::new(DumbExit {}),
    }
}
