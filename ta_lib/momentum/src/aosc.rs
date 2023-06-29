use overlap::sma::sma;
use price::median::median_price;

pub fn aosc(
    high: &[f64],
    low: &[f64],
    short_period: usize,
    long_period: usize,
) -> Vec<Option<f64>> {
    let median_price = median_price(high, low);
    let median_price_values = median_price
        .iter()
        .map(|&x| x.unwrap_or(0.0))
        .collect::<Vec<_>>();

    let ao_short = sma(&median_price_values, short_period);
    let ao_long = sma(&median_price_values, long_period);

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

    #[test]
    fn test_aosc() {
        let high = &[3.0, 4.0, 5.0, 6.0, 7.0];
        let low = &[1.0, 2.0, 3.0, 4.0, 5.0];

        let short_period = 2;
        let long_period = 4;

        let result = aosc(high, low, short_period, long_period);

        let expected_result = vec![None, None, None, Some(1.0), Some(1.0)];

        assert_eq!(result, expected_result);
    }
}
