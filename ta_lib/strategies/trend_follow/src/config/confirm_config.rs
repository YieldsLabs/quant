use serde::Deserialize;

#[derive(Deserialize)]
#[serde(tag = "type")]
pub enum ConfirmConfig {
    Dpo {
        source_type: f32,
        smooth_type: f32,
        period: f32,
    },
    Eom {
        source_type: f32,
        smooth_type: f32,
        period: f32,
        divisor: f32,
    },
    Cci {
        source_type: f32,
        smooth_type: f32,
        period: f32,
        factor: f32,
    },
    Dumb {
        period: f32,
    },
    RsiNeutrality {
        source_type: f32,
        smooth_type: f32,
        period: f32,
        threshold: f32,
    },
    RsiSignalLine {
        source_type: f32,
        smooth_type: f32,
        period: f32,
        smooth_signal: f32,
        smooth_period: f32,
        threshold: f32,
    },
    Roc {
        source_type: f32,
        period: f32,
    },
    Stc {
        source_type: f32,
        smooth_type: f32,
        fast_period: f32,
        slow_period: f32,
        cycle: f32,
        d_first: f32,
        d_second: f32,
    },
    Dso {
        source_type: f32,
        smooth_type: f32,
        smooth_period: f32,
        k_period: f32,
        d_period: f32,
    },
    Vi {
        atr_period: f32,
        period: f32,
    },
}
