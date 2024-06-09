use core::prelude::*;

pub fn snatr(
    atr: &Series<f32>,
    period: usize,
    smooth_type: Smooth,
    smooth_period: usize,
) -> Series<f32> {
    atr.normalize(period).smooth(smooth_type, smooth_period)
}

#[test]
fn test_snatr() {
    use crate::atr;

    let high = Series::from([
        19.129, 19.116, 19.154, 19.195, 19.217, 19.285, 19.341, 19.394, 19.450,
    ]);
    let low = Series::from([
        19.090, 19.086, 19.074, 19.145, 19.141, 19.155, 19.219, 19.306, 19.355,
    ]);
    let close = Series::from([
        19.102, 19.100, 19.146, 19.181, 19.155, 19.248, 19.309, 19.355, 19.439,
    ]);
    let atr_period = 3;
    let atr = atr(&high, &low, &close, Smooth::SMMA, atr_period);
    let period = 3;
    let epsilon = 0.001;
    let expected = [
        0.0, 0.0, 0.5, 0.8257546, 0.99494743, 0.9974737, 1.0, 0.9014031, 0.5520136,
    ];

    let result: Vec<f32> = snatr(&atr, atr_period, Smooth::WMA, period).into();

    for i in 0..high.len() {
        assert!(
            (result[i] - expected[i]).abs() < epsilon,
            "at position {}: {} != {}",
            i,
            result[i],
            expected[i]
        )
    }
}
