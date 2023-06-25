use statistics::stddev::std_dev;

pub fn vama(
    close: &[f64],
    short_volatility: usize,
    long_volatility: usize,
    alpha_factor: f64,
) -> Vec<Option<f64>> {
    let short_std = std_dev(close, short_volatility);
    let long_std = std_dev(close, long_volatility);

    let mut alpha = vec![None; close.len()];
    let mut vama = vec![None; close.len()];

    for i in 0..close.len() {
        if let (Some(ss), Some(ls)) = (short_std[i], long_std[i]) {
            alpha[i] = Some((ss / ls) * alpha_factor);
        }
    }

    let alpha = alpha.iter().filter_map(|&x| x).collect::<Vec<_>>();

    vama = ema(&alpha, short_volatility);

    vama
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_vama() {
        let close = vec![100.0, 105.0, 110.0, 115.0, 120.0];
        let short_volatility = 2;
        let long_volatility = 3;
        let alpha_factor = 0.5;
        let expected = vec![
            None,
            Some(102.5),
            Some(106.25),
            Some(110.625),
            Some(115.3125),
        ];
        let result = vama(&close, short_volatility, long_volatility, alpha_factor);
        assert_eq!(result, expected);
    }
}
