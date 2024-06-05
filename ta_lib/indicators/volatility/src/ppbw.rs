use crate::ppb;
use core::prelude::*;

pub fn ppbw(
    source: &Series<f32>,
    high: &Series<f32>,
    low: &Series<f32>,
    smooth_type: Smooth,
    period: usize,
    factor: f32,
) -> Series<f32> {
    let (upb, mb, lb) = ppb(source, high, low, smooth_type, period, factor);

    SCALE * (upb - lb) / mb
}

#[test]
fn test_ppbw() {
    let source = Series::from([
        19.102, 19.100, 19.146, 19.181, 19.155, 19.248, 19.309, 19.355, 19.439,
    ]);
    let high = Series::from([
        19.129, 19.116, 19.154, 19.195, 19.217, 19.285, 19.341, 19.394, 19.450,
    ]);
    let low = Series::from([
        19.090, 19.086, 19.074, 19.145, 19.141, 19.155, 19.219, 19.306, 19.355,
    ]);
    let factor = 2.0;
    let period = 3;
    let expected = [
        0.0, 0.081802, 0.17339352, 0.39918908, 0.39880714, 0.40701413, 0.5263783, 0.52456045,
        0.8744923,
    ];

    let result: Vec<f32> = ppbw(&source, &high, &low, Smooth::SMA, period, factor).into();

    assert_eq!(result, expected);
}
