use overlap::{ema::ema, sma::sma, smma::smma, wma::wma};
use utils::tr::true_range;

pub fn atr(
    high: &[f64],
    low: &[f64],
    close: &[f64],
    period: usize,
    smothing: Option<&str>,
) -> Vec<Option<f64>> {
    let tr = true_range(high, low, close);

    match smothing {
        Some("SMMA") => smma(&tr, period),
        Some("SMA") => sma(&tr, period),
        Some("EMA") => ema(&tr, period),
        _ => wma(&tr, period),
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
        let smothing = Some("SMMA");
        let expected = vec![None, None, Some(1.5555)];

        let result = atr(&high, &low, &close, period, smothing);

        assert_eq!(result, expected);
    }
}
