use serde::Deserialize;

#[derive(Deserialize)]
#[serde(tag = "type")]
pub enum PulseConfig {
    Adx {
        smooth_type: f32,
        adx_period: f32,
        di_period: f32,
        threshold: f32,
    },
    Dumb {
        period: f32,
    },
    Chop {
        period: f32,
        atr_period: f32,
        threshold: f32,
    },
    Nvol {
        smooth_type: f32,
        period: f32,
    },
    Vo {
        smooth_type: f32,
        fast_period: f32,
        slow_period: f32,
    },
    Tdfi {
        source_type: f32,
        smooth_type: f32,
        period: f32,
        n: f32,
    },
    Wae {
        smooth_type: f32,
        fast_period: f32,
        slow_period: f32,
        smooth_bb: f32,
        bb_period: f32,
        factor: f32,
        strength: f32,
    },
}
