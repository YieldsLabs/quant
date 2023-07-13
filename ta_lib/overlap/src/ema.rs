use core::series::Series;

pub fn ema(source: &[f64], period: usize) -> Series<f64> {
    let len = source.len();
    let alpha = 2.0 / (period as f64 + 1.0);
    let one_minus_alpha = 1.0 - alpha;

    let mut ema = Series::empty(len);

    ema[0] = Some(source[0]);

    for i in 1..len {
        let ema_prev = ema[i - 1].unwrap_or(0.0);
        ema[i] = Some(alpha * source[i] + one_minus_alpha * ema_prev);
    }

    ema
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_ema() {
        let source = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let expected = vec![Some(1.0), Some(1.5), Some(2.25), Some(3.125), Some(4.0625)];

        let result = ema(&source, 3);

        assert_eq!(result, expected);
    }
}
