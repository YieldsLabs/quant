use serde::Deserialize;

#[derive(Deserialize)]
#[serde(tag = "type")]
pub enum PulseConfig {
    Adx {
        smooth: f32,
        period: f32,
        period_di: f32,
        threshold: f32,
    },
    Dumb {
        period: f32,
    },
    Chop {
        period: f32,
        smooth_atr: f32,
        period_atr: f32,
        threshold: f32,
    },
    Nvol {
        smooth: f32,
        period: f32,
    },
    Vo {
        smooth: f32,
        period_fast: f32,
        period_slow: f32,
    },
    Tdfi {
        source: f32,
        smooth: f32,
        period: f32,
        n: f32,
    },
    Wae {
        source: f32,
        smooth: f32,
        period_fast: f32,
        period_slow: f32,
        smooth_bb: f32,
        period_bb: f32,
        factor: f32,
        strength: f32,
    },
    Yz {
        period: f32,
        smooth_signal: f32,
        period_signal: f32,
    },
    Sqz {
        source: f32,
        smooth: f32,
        period: f32,
        smooth_atr: f32,
        period_atr: f32,
        factor_bb: f32,
        factor_kch: f32,
    },
}
