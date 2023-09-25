use core::Series;
use trend::{ema, sma, smma, wma};
use utils::tr;

pub fn atr(
    high: &Series<f32>,
    low: &Series<f32>,
    close: &Series<f32>,
    period: usize,
    smoothing: Option<&str>,
) -> Series<f32> {
    let tr = tr(high, low, close);

    match smoothing {
        Some("WMA") => wma(&tr, period),
        Some("SMA") => sma(&tr, period),
        Some("EMA") => ema(&tr, period),
        Some("SMMA") | _ => smma(&tr, period),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_atr_smma() {
        let high = Series::from([
            19.129, 19.116, 19.154, 19.195, 19.217, 19.285, 19.341, 19.394, 19.450,
        ]);
        let low = Series::from([
            19.090, 19.086, 19.074, 19.145, 19.141, 19.155, 19.219, 19.306, 19.355,
        ]);
        let close = Series::from([
            19.102, 19.100, 19.146, 19.181, 19.155, 19.248, 19.309, 19.355, 19.439,
        ]);
        let period = 3;
        let epsilon = 0.001;
        let smothing = None;
        let expected = [
            0.0,
            0.009999594,
            0.033333037,
            0.038888436,
            0.051258393,
            0.07750531,
            0.09233679,
            0.09001309,
            0.091675796,
        ];

        let result: Vec<f32> = atr(&high, &low, &close, period, smothing).into();

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
}
