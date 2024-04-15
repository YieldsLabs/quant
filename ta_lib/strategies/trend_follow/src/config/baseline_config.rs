use serde::Deserialize;

#[derive(Deserialize)]
#[serde(tag = "type")]
pub enum BaseLineConfig {
    Ma { ma: f32, period: f32 },
}
