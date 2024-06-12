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
        PulseConfig::Braid {
            smooth_type,
            fast_period,
            slow_period,
            open_period,
            strength,
            atr_period,
        } => Box::new(BraidPulse::new(
            smooth_deserialize(smooth_type as usize),
            fast_period,
            slow_period,
            open_period,
            strength,
            atr_period,
        )),
        PulseConfig::Chop {
            period,
            atr_period,
            threshold,
        } => Box::new(ChopPulse::new(period, atr_period, threshold)),
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
            atr_period,
            dz_factor,
        } => Box::new(WaePulse::new(
            smooth_deserialize(smooth_type as usize),
            fast_period,
            slow_period,
            smooth_deserialize(smooth_bb as usize),
            bb_period,
            factor,
            strength,
            atr_period,
            dz_factor,
        )),
    }
}
