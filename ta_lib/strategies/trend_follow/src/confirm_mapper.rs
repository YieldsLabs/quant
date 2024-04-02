use crate::smooth_mapper::map_to_smooth;
use base::prelude::*;
use confirm::*;
use serde::Deserialize;

#[derive(Deserialize)]
#[serde(tag = "type")]
pub enum ConfirmConfig {
    Dpo {
        smooth_type: f32,
        period: f32,
    },
    Eom {
        smooth_type: f32,
        period: f32,
        divisor: f32,
    },
    Cci {
        smooth_type: f32,
        period: f32,
        factor: f32,
    },
    Dumb {
        period: f32,
    },
    Rsi {
        smooth_type: f32,
        period: f32,
        smooth_signal: f32,
        smooth_period: f32,
        threshold: f32,
    },
    Roc {
        period: f32,
    },
    Stc {
        smooth_type: f32,
        fast_period: f32,
        slow_period: f32,
        cycle: f32,
        d_first: f32,
        d_second: f32,
    },
    Dso {
        smooth_type: f32,
        smooth_period: f32,
        k_period: f32,
        d_period: f32,
    },
}

pub fn map_to_confirm(config: ConfirmConfig) -> Box<dyn Confirm> {
    match config {
        ConfirmConfig::Dpo {
            smooth_type,
            period,
        } => Box::new(DPOConfirm::new(map_to_smooth(smooth_type as usize), period)),
        ConfirmConfig::Dso {
            smooth_type,
            smooth_period,
            k_period,
            d_period,
        } => Box::new(DSOConfirm::new(
            map_to_smooth(smooth_type as usize),
            smooth_period,
            k_period,
            d_period,
        )),
        ConfirmConfig::Cci {
            smooth_type,
            period,
            factor,
        } => Box::new(CCIConfirm::new(
            map_to_smooth(smooth_type as usize),
            period,
            factor,
        )),
        ConfirmConfig::Eom {
            smooth_type,
            period,
            divisor,
        } => Box::new(EOMConfirm::new(
            map_to_smooth(smooth_type as usize),
            period,
            divisor,
        )),
        ConfirmConfig::Dumb { period } => Box::new(DumbConfirm::new(period)),
        ConfirmConfig::Rsi {
            smooth_type,
            period,
            smooth_signal,
            smooth_period,
            threshold,
        } => Box::new(RSIConfirm::new(
            map_to_smooth(smooth_type as usize),
            period,
            map_to_smooth(smooth_signal as usize),
            smooth_period,
            threshold,
        )),
        ConfirmConfig::Roc { period } => Box::new(ROCConfirm::new(period)),
        ConfirmConfig::Stc {
            smooth_type,
            fast_period,
            slow_period,
            cycle,
            d_first,
            d_second,
        } => Box::new(STCConfirm::new(
            map_to_smooth(smooth_type as usize),
            fast_period,
            slow_period,
            cycle,
            d_first,
            d_second,
        )),
    }
}
