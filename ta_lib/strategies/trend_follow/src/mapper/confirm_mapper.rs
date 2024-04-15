use crate::config::ConfirmConfig;
use crate::deserialize::smooth_deserialize;
use base::prelude::*;
use confirm::*;

#[inline]
pub fn map_to_confirm(config: ConfirmConfig) -> Box<dyn Confirm> {
    match config {
        ConfirmConfig::Dpo {
            smooth_type,
            period,
        } => Box::new(DpoConfirm::new(
            smooth_deserialize(smooth_type as usize),
            period,
        )),
        ConfirmConfig::Dso {
            smooth_type,
            smooth_period,
            k_period,
            d_period,
        } => Box::new(DsoConfirm::new(
            smooth_deserialize(smooth_type as usize),
            smooth_period,
            k_period,
            d_period,
        )),
        ConfirmConfig::Cci {
            smooth_type,
            period,
            factor,
        } => Box::new(CciConfirm::new(
            smooth_deserialize(smooth_type as usize),
            period,
            factor,
        )),
        ConfirmConfig::Eom {
            smooth_type,
            period,
            divisor,
        } => Box::new(EomConfirm::new(
            smooth_deserialize(smooth_type as usize),
            period,
            divisor,
        )),
        ConfirmConfig::Dumb { period } => Box::new(DumbConfirm::new(period)),
        ConfirmConfig::RsiSignalLine {
            smooth_type,
            period,
            smooth_signal,
            smooth_period,
            threshold,
        } => Box::new(RsiSignalLineConfirm::new(
            smooth_deserialize(smooth_type as usize),
            period,
            smooth_deserialize(smooth_signal as usize),
            smooth_period,
            threshold,
        )),
        ConfirmConfig::RsiNeutrality {
            smooth_type,
            period,
            threshold,
        } => Box::new(RsiNeutralityConfirm::new(
            smooth_deserialize(smooth_type as usize),
            period,
            threshold,
        )),
        ConfirmConfig::Roc { period } => Box::new(RocConfirm::new(period)),
        ConfirmConfig::Vi { atr_period, period } => Box::new(ViConfirm::new(atr_period, period)),
        ConfirmConfig::Stc {
            smooth_type,
            fast_period,
            slow_period,
            cycle,
            d_first,
            d_second,
        } => Box::new(StcConfirm::new(
            smooth_deserialize(smooth_type as usize),
            fast_period,
            slow_period,
            cycle,
            d_first,
            d_second,
        )),
    }
}
