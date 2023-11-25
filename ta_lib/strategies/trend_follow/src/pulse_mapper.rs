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
    Osc {
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
        PulseConfig::Dumb { period } => Box::new(DumbPulse::new(period)),
        PulseConfig::Osc {
            short_period,
            long_period,
        } => Box::new(OSCPulse::new(short_period, long_period)),
    }
}
