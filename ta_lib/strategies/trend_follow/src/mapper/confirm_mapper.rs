use crate::config::ConfirmConfig;
use crate::deserialize::{smooth_deserialize, source_deserialize};
use base::prelude::*;
use confirm::*;

#[inline]
pub fn map_to_confirm(config: ConfirmConfig) -> Box<dyn Confirm> {
    match config {
        // contrarian
        ConfirmConfig::BbC {
            smooth,
            period,
            factor,
        } => Box::new(BbConfirm::new(
            smooth_deserialize(smooth as usize),
            period,
            factor,
        )),
        // trend
        ConfirmConfig::Dpo {
            source_type,
            smooth_type,
            period,
        } => Box::new(DpoConfirm::new(
            source_deserialize(source_type as usize),
            smooth_deserialize(smooth_type as usize),
            period,
        )),
        ConfirmConfig::Cc {
            source,
            period_fast,
            period_slow,
            smooth,
            period_smooth,
            smooth_signal,
            period_signal,
        } => Box::new(CcConfirm::new(
            source_deserialize(source as usize),
            period_fast,
            period_slow,
            smooth_deserialize(smooth as usize),
            period_smooth,
            smooth_deserialize(smooth_signal as usize),
            period_signal,
        )),
        ConfirmConfig::Cci {
            source,
            period,
            factor,
            smooth,
            period_smooth,
        } => Box::new(CciConfirm::new(
            source_deserialize(source as usize),
            period,
            factor,
            smooth_deserialize(smooth as usize),
            period_smooth,
        )),
        ConfirmConfig::Wpr {
            source,
            period,
            smooth_signal,
            period_signal,
        } => Box::new(WprConfirm::new(
            source_deserialize(source as usize),
            period,
            smooth_deserialize(smooth_signal as usize),
            period_signal,
        )),
        ConfirmConfig::Eom {
            source_type,
            smooth_type,
            period,
        } => Box::new(EomConfirm::new(
            source_deserialize(source_type as usize),
            smooth_deserialize(smooth_type as usize),
            period,
        )),
        ConfirmConfig::Dumb { period } => Box::new(DumbConfirm::new(period)),
        ConfirmConfig::RsiSignalLine {
            source_type,
            smooth_type,
            period,
            smooth_signal,
            smooth_period,
            threshold,
        } => Box::new(RsiSignalLineConfirm::new(
            source_deserialize(source_type as usize),
            smooth_deserialize(smooth_type as usize),
            period,
            smooth_deserialize(smooth_signal as usize),
            smooth_period,
            threshold,
        )),
        ConfirmConfig::RsiNeutrality {
            source_type,
            smooth_type,
            period,
            threshold,
        } => Box::new(RsiNeutralityConfirm::new(
            source_deserialize(source_type as usize),
            smooth_deserialize(smooth_type as usize),
            period,
            threshold,
        )),
        ConfirmConfig::Stc {
            source_type,
            smooth_type,
            fast_period,
            slow_period,
            cycle,
            d_first,
            d_second,
        } => Box::new(StcConfirm::new(
            source_deserialize(source_type as usize),
            smooth_deserialize(smooth_type as usize),
            fast_period,
            slow_period,
            cycle,
            d_first,
            d_second,
        )),
        ConfirmConfig::Braid {
            smooth_type,
            fast_period,
            slow_period,
            open_period,
            strength,
            smooth_atr,
            period_atr,
        } => Box::new(BraidConfirm::new(
            smooth_deserialize(smooth_type as usize),
            fast_period,
            slow_period,
            open_period,
            strength,
            smooth_deserialize(smooth_atr as usize),
            period_atr,
        )),
        ConfirmConfig::Didi {
            source,
            smooth,
            period_medium,
            period_slow,
            smooth_signal,
            period_signal,
        } => Box::new(DidiConfirm::new(
            source_deserialize(source as usize),
            smooth_deserialize(smooth as usize),
            period_medium,
            period_slow,
            smooth_deserialize(smooth_signal as usize),
            period_signal,
        )),
    }
}
