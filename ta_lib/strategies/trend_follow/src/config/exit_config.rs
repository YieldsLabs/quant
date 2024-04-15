use serde::Deserialize;

#[derive(Deserialize)]
#[serde(tag = "type")]
pub enum ExitConfig {
    Ast {
        atr_period: f32,
        factor: f32,
    },
    Cci {
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
        smooth_type: f32,
        period: f32,
        threshold: f32,
    },
    Ma {
        ma: f32,
        period: f32,
    },
    Mfi {
        period: f32,
        threshold: f32,
    },
    Trix {
        smooth_type: f32,
        period: f32,
        signal_period: f32,
    },
}
