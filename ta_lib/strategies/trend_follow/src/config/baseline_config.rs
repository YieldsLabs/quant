use serde::Deserialize;

#[derive(Deserialize)]
#[serde(tag = "type")]
pub enum BaseLineConfig {
    Ma {
        source_type: f32,
        ma: f32,
        period: f32,
    },
}
