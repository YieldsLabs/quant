use core::series::Series;

pub fn aosc(hl2: &[f32], short_period: usize, long_period: usize) -> Series<f32> {
    let hl2 = Series::from(hl2);

    let ao_short = hl2.ma(short_period);
    let ao_long = hl2.ma(long_period);

    let aosc = ao_short - ao_long;

    aosc
}

#[cfg(test)]
mod tests {
    use super::*;
    use price::median_price;

    #[test]
    fn test_aosc() {
        let high = vec![3.0, 4.0, 5.0, 6.0, 7.0];
        let low = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let hl2 = median_price(&high, &low);
        let short_period = 2;
        let long_period = 4;
        let expected = vec![0.0, 0.0, 0.5, 1.0, 1.0];

        let result: Vec<f32> = aosc(&hl2, short_period, long_period).into();

        assert_eq!(result, expected);
    }
}
