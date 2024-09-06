use crate::config::PulseConfig;
use crate::deserialize::{smooth_deserialize, source_deserialize};
use base::prelude::*;
use pulse::*;

#[inline]
pub fn map_to_pulse(config: PulseConfig) -> Box<dyn Pulse> {
    match config {
        PulseConfig::Adx {
            smooth,
            period,
            period_di,
            threshold,
        } => Box::new(AdxPulse::new(
            smooth_deserialize(smooth as usize),
            period,
            period_di,
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
        PulseConfig::Nvol { smooth, period } => {
            Box::new(NvolPulse::new(smooth_deserialize(smooth as usize), period))
        }
        PulseConfig::Tdfi {
            source,
            smooth,
            period,
            n,
        } => Box::new(TdfiPulse::new(
            source_deserialize(source as usize),
            smooth_deserialize(smooth as usize),
            period,
            n,
        )),
        PulseConfig::Vo {
            smooth,
            period_fast,
            period_slow,
        } => Box::new(VoPulse::new(
            smooth_deserialize(smooth as usize),
            period_fast,
            period_slow,
        )),
        PulseConfig::Wae {
            source,
            smooth,
            period_fast,
            period_slow,
            smooth_bb,
            period_bb,
            factor,
            strength,
        } => Box::new(WaePulse::new(
            source_deserialize(source as usize),
            smooth_deserialize(smooth as usize),
            period_fast,
            period_slow,
            smooth_deserialize(smooth_bb as usize),
            period_bb,
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
        PulseConfig::Sqz {
            source,
            smooth,
            period,
            smooth_atr,
            period_atr,
            factor_bb,
            factor_kch,
        } => Box::new(SqzPulse::new(
            source_deserialize(source as usize),
            smooth_deserialize(smooth as usize),
            period,
            smooth_deserialize(smooth_atr as usize),
            period_atr,
            factor_bb,
            factor_kch,
        )),
    }
}
