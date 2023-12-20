use base::OHLCVSeries;
use core::prelude::*;
use momentum::stochosc;

pub enum StochType {
    STOCHOSC,
}

pub fn stoch_indicator(
    stoch_type: &StochType,
    data: &OHLCVSeries,
    period: usize,
    k_period: usize,
    d_period: usize,
) -> (Series<f32>, Series<f32>) {
    match stoch_type {
        StochType::STOCHOSC => stochosc(
            &data.high,
            &data.low,
            &data.close,
            period,
            k_period,
            d_period,
        ),
    }
}
