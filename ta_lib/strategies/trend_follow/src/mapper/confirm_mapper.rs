use crate::config::ConfirmConfig;
use crate::deserialize::{smooth_deserialize, source_deserialize};
use base::prelude::*;
use confirm::*;

#[inline]
pub fn map_to_confirm(config: ConfirmConfig) -> Box<dyn Confirm> {
    match config {
        ConfirmConfig::Dpo {
            source_type,
            smooth_type,
            period,
        } => Box::new(DpoConfirm::new(
            source_deserialize(source_type as usize),
            smooth_deserialize(smooth_type as usize),
            period,
        )),
        ConfirmConfig::Dso {
            source_type,
            smooth_type,
            smooth_period,
            k_period,
            d_period,
        } => Box::new(DsoConfirm::new(
            source_deserialize(source_type as usize),
            smooth_deserialize(smooth_type as usize),
            smooth_period,
            k_period,
            d_period,
        )),
        ConfirmConfig::Cci {
            source_type,
            smooth_type,
            period,
            factor,
        } => Box::new(CciConfirm::new(
            source_deserialize(source_type as usize),
            smooth_deserialize(smooth_type as usize),
            period,
            factor,
        )),
        ConfirmConfig::Eom {
            source_type,
            smooth_type,
            period,
            divisor,
        } => Box::new(EomConfirm::new(
            source_deserialize(source_type as usize),
            smooth_deserialize(smooth_type as usize),
            period,
            divisor,
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
        ConfirmConfig::Roc {
            source_type,
            period,
        } => Box::new(RocConfirm::new(
            source_deserialize(source_type as usize),
            period,
        )),
        ConfirmConfig::Vi { atr_period, period } => Box::new(ViConfirm::new(atr_period, period)),
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
    }
}
