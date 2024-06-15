use crate::config::PulseConfig;
use crate::deserialize::{smooth_deserialize, source_deserialize};
use base::prelude::*;
use pulse::*;

#[inline]
pub fn map_to_pulse(config: PulseConfig) -> Box<dyn Pulse> {
    match config {
        PulseConfig::Adx {
            smooth_type,
            adx_period,
            di_period,
            threshold,
        } => Box::new(AdxPulse::new(
            smooth_deserialize(smooth_type as usize),
            adx_period,
            di_period,
            threshold,
        )),
        PulseConfig::Chop {
            period,
            smooth_atr,
            period_atr,
            threshold,
        } => Box::new(ChopPulse::new(
            period,
            smooth_deserialize(smooth_atr as usize),
            period_atr,
            threshold,
        )),
        PulseConfig::Dumb { period } => Box::new(DumbPulse::new(period)),
        PulseConfig::Nvol {
            smooth_type,
            period,
        } => Box::new(NvolPulse::new(
            smooth_deserialize(smooth_type as usize),
            period,
        )),
        PulseConfig::Tdfi {
            source_type,
            smooth_type,
            period,
            n,
        } => Box::new(TdfiPulse::new(
            source_deserialize(source_type as usize),
            smooth_deserialize(smooth_type as usize),
            period,
            n,
        )),
        PulseConfig::Vo {
            smooth_type,
            fast_period,
            slow_period,
        } => Box::new(VoPulse::new(
            smooth_deserialize(smooth_type as usize),
            fast_period,
            slow_period,
        )),
        PulseConfig::Wae {
            smooth_type,
            fast_period,
            slow_period,
            smooth_bb,
            bb_period,
            factor,
            strength,
        } => Box::new(WaePulse::new(
            smooth_deserialize(smooth_type as usize),
            fast_period,
            slow_period,
            smooth_deserialize(smooth_bb as usize),
            bb_period,
            factor,
            strength,
        )),
        PulseConfig::Yz {
            period,
            smooth_signal,
            period_signal,
        } => Box::new(YzPulse::new(
            period,
            smooth_deserialize(smooth_signal as usize),
            period_signal,
        )),
    }
}
