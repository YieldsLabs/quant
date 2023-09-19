use crate::atr;
use core::series::Series;

pub fn snatr(
    high: &[f32],
    low: &[f32],
    close: &[f32],
    atr_period: usize,
    period: usize,
) -> Series<f32> {
    let atr = atr(&high, &low, &close, atr_period, None);

    let snatr = (&atr - &atr.lowest(atr_period))
        / (&atr.highest(atr_period) - &atr.lowest(atr_period)).wma(period);

    snatr
}

#[test]
    fn test_snatr() {
        let high = vec![19.129, 19.116, 19.154, 19.195, 19.217, 19.285, 19.341, 19.394, 19.450];
        let low = vec![19.090, 19.086, 19.074, 19.145, 19.141, 19.155, 19.219, 19.306, 19.355];
        let close = vec![19.102, 19.100, 19.146, 19.181, 19.155, 19.248, 19.309, 19.355, 19.439];
        let atr_period = 3;
        let period = 3;
        let epsilon = 0.001;
        let expected = vec![0.0, 0.0, 1.6666753, 1.0612303, 0.7423184, 1.2830225, 1.1285568, 0.48596168, 0.109491356];

        let result: Vec<f32> = snatr(&high, &low, &close, atr_period, period).into();

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
