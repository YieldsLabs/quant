use serde::Deserialize;

#[derive(Deserialize)]
#[serde(tag = "type")]
pub enum StopLossConfig {
    Atr { period: f32, factor: f32 },
    Dch { period: f32, factor: f32 },
}
