use base::prelude::*;
use confirm::*;
use serde::Deserialize;

#[derive(Deserialize)]
#[serde(tag = "type")]
pub enum ConfirmConfig {
    Dpo {
        period: f32,
    },
    Eom {
        period: f32,
        divisor: f32,
    },
    Dumb {
        period: f32,
    },
    Rsi {
        period: f32,
        threshold: f32,
    },
    Stc {
        fast_period: f32,
        slow_period: f32,
        cycle: f32,
        d_first: f32,
        d_second: f32,
    },
}

pub fn map_to_confirm(config: ConfirmConfig) -> Box<dyn Confirm> {
    match config {
        ConfirmConfig::Dpo { period } => Box::new(DPOConfirm::new(period)),
        ConfirmConfig::Eom { period, divisor } => Box::new(EOMConfirm::new(period, divisor)),
        ConfirmConfig::Dumb { period } => Box::new(DumbConfirm::new(period)),
        ConfirmConfig::Rsi { period, threshold } => Box::new(RSIConfirm::new(period, threshold)),
        ConfirmConfig::Stc {
            fast_period,
            slow_period,
            cycle,
            d_first,
            d_second,
        } => Box::new(STCConfirm::new(
            fast_period,
            slow_period,
            cycle,
            d_first,
            d_second,
        )),
    }
}
