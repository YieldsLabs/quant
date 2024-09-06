use serde::Deserialize;

#[derive(Deserialize)]
#[serde(tag = "type")]
pub enum StopLossConfig {
    Atr {
        smooth: f32,
        period: f32,
        factor: f32,
    },
    Dch {
        period: f32,
        factor: f32,
    },
}
