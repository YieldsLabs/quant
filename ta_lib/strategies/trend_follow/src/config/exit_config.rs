use serde::Deserialize;

#[derive(Deserialize)]
#[serde(tag = "type")]
pub enum ExitConfig {
    Ast {
        source_type: f32,
        atr_period: f32,
        factor: f32,
    },
    Cci {
        source_type: f32,
        smooth_type: f32,
        period: f32,
        factor: f32,
        threshold: f32,
    },
    Dumb {},
    HighLow {
        period: f32,
    },
    Rsi {
        source_type: f32,
        smooth_type: f32,
        period: f32,
        threshold: f32,
    },
    Ma {
        source_type: f32,
        ma: f32,
        period: f32,
    },
    Mfi {
        source_type: f32,
        period: f32,
        threshold: f32,
    },
    Trix {
        source_type: f32,
        smooth_type: f32,
        period: f32,
        signal_period: f32,
    },
}
