use core::series::Series;
use trend::{ema, sma, smma, wma};
use utils::true_range;

pub fn atr(
    high: &[f32],
    low: &[f32],
    close: &[f32],
    period: usize,
    smothing: Option<&str>,
) -> Series<f32> {
    let tr = true_range(high, low, close);

    match smothing {
        Some("WMA") => wma(&tr, period),
        Some("SMA") => sma(&tr, period),
        Some("EMA") => ema(&tr, period),
        Some("SMMA") => smma(&tr, period),
        _ => smma(&tr, period),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_atr_smma() {
        let high = vec![2.0, 4.0, 6.0];
        let low = vec![1.0, 2.0, 3.0];
        let close = vec![1.5, 3.0, 4.5];
        let period = 3;
        let epsilon = 0.001;
        let smothing = None;
        let expected = vec![0.0, 0.8333, 1.5555];

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
