use serde::Deserialize;

#[derive(Deserialize)]
#[serde(tag = "type")]
pub enum ExitConfig {
    Ast {
        source_type: f32,
        smooth_atr: f32,
        period_atr: f32,
        factor: f32,
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
    Rex {
        source: f32,
        smooth: f32,
        period: f32,
        smooth_signal: f32,
        period_signal: f32,
    },
    Mad {
        source: f32,
        period_fast: f32,
        period_slow: f32,
    },
}
