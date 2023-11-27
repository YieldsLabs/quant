use base::Pulse;
use pulse::*;
use serde::Deserialize;

#[derive(Deserialize)]
#[serde(tag = "type")]
pub enum PulseConfig {
    Adx {
        adx_period: f32,
        di_period: f32,
        threshold: f32,
    },
    Dumb {
        period: f32,
    },
    Chop {
        atr_period: f32,
        period: f32,
        threshold: f32,
    },
    Vo {
        short_period: f32,
        long_period: f32,
    },
}

pub fn map_to_pulse(config: PulseConfig) -> Box<dyn Pulse> {
    match config {
        PulseConfig::Adx {
            adx_period,
            di_period,
            threshold,
        } => Box::new(ADXPulse::new(adx_period, di_period, threshold)),
        PulseConfig::Chop {
            atr_period,
            period,
            threshold,
        } => Box::new(CHOPPulse::new(atr_period, period, threshold)),
        PulseConfig::Dumb { period } => Box::new(DumbPulse::new(period)),
        PulseConfig::Vo {
            short_period,
            long_period,
        } => Box::new(VoPulse::new(short_period, long_period)),
    }
}
