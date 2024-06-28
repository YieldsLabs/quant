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
    },
    Cci {
        source: f32,
        period: f32,
        factor: f32,
        smooth: f32,
        period_smooth: f32,
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
    Stc {
        source_type: f32,
        smooth_type: f32,
        fast_period: f32,
        slow_period: f32,
        cycle: f32,
        d_first: f32,
        d_second: f32,
    },
    Braid {
        smooth_type: f32,
        fast_period: f32,
        slow_period: f32,
        open_period: f32,
        strength: f32,
        smooth_atr: f32,
        period_atr: f32,
    },
    Wpr {
        source: f32,
        period: f32,
        smooth_signal: f32,
        period_signal: f32,
    },
    Didi {
        source: f32,
        smooth: f32,
        period_medium: f32,
        period_slow: f32,
        smooth_signal: f32,
        period_signal: f32,
    },
    Cc {
        source: f32,
        period_fast: f32,
        period_slow: f32,
        smooth: f32,
        period_smooth: f32,
        smooth_signal: f32,
        period_signal: f32,
    },
}
