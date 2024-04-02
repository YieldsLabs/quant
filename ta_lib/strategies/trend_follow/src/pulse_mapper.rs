use crate::smooth_mapper::map_to_smooth;
use base::prelude::*;
use pulse::*;
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
    Braid {
        smooth_type: f32,
        fast_period: f32,
        slow_period: f32,
        open_period: f32,
        strength: f32,
        atr_period: f32,
    },
    Dumb {
        period: f32,
    },
    Chop {
        atr_period: f32,
        period: f32,
        threshold: f32,
    },
    Nvol {
        smooth_type: f32,
        period: f32,
    },
    Vo {
        smooth_type: f32,
        short_period: f32,
        long_period: f32,
    },
    Tdfi {
        smooth_type: f32,
        period: f32,
        n: f32,
    },
}

pub fn map_to_pulse(config: PulseConfig) -> Box<dyn Pulse> {
    match config {
        PulseConfig::Adx {
            smooth_type,
            adx_period,
            di_period,
            threshold,
        } => Box::new(ADXPulse::new(
            map_to_smooth(smooth_type as usize),
            adx_period,
            di_period,
            threshold,
        )),
        PulseConfig::Braid {
            smooth_type,
            fast_period,
            slow_period,
            open_period,
            strength,
            atr_period,
        } => Box::new(BraidPulse::new(
            map_to_smooth(smooth_type as usize),
            fast_period,
            slow_period,
            open_period,
            strength,
            atr_period,
        )),
        PulseConfig::Chop {
            atr_period,
            period,
            threshold,
        } => Box::new(CHOPPulse::new(atr_period, period, threshold)),
        PulseConfig::Dumb { period } => Box::new(DumbPulse::new(period)),
        PulseConfig::Nvol {
            smooth_type,
            period,
        } => Box::new(NvolPulse::new(map_to_smooth(smooth_type as usize), period)),
        PulseConfig::Tdfi {
            smooth_type,
            period,
            n,
        } => Box::new(TDFIPulse::new(
            map_to_smooth(smooth_type as usize),
            period,
            n,
        )),
        PulseConfig::Vo {
            smooth_type,
            short_period,
            long_period,
        } => Box::new(VoPulse::new(
            map_to_smooth(smooth_type as usize),
            short_period,
            long_period,
        )),
    }
}
