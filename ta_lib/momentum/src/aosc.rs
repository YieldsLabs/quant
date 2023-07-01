use overlap::sma::sma;

pub fn aosc(hl2: &[f64], short_period: usize, long_period: usize) -> Vec<Option<f64>> {
    let ao_short = sma(hl2, short_period);
    let ao_long = sma(hl2, long_period);

    ao_short
        .iter()
        .zip(&ao_long)
        .map(|(&short, &long)| match (short, long) {
            (Some(short), Some(long)) => Some(short - long),
            _ => None,
        })
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;
    use price::median::median_price;

    #[test]
    fn test_aosc() {
        let high = &[3.0, 4.0, 5.0, 6.0, 7.0];
        let low = &[1.0, 2.0, 3.0, 4.0, 5.0];
        let hl2 = median_price(high, low);
        let short_period = 2;
        let long_period = 4;
        let expected_result = vec![None, None, None, Some(1.0), Some(1.0)];

        let result = aosc(&hl2, short_period, long_period);

        assert_eq!(result, expected_result);
    }
}
