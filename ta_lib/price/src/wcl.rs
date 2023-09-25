use core::Series;

pub fn wcl(high: &Series<f32>, low: &Series<f32>, close: &Series<f32>) -> Series<f32> {
    (high + low + (close * 2.0)) / 4.0
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_weighted_close_price() {
        let high = Series::from([1.0, 2.0, 3.0]);
        let low = Series::from([0.5, 1.0, 1.5]);
        let close = Series::from([0.75, 1.5, 2.25]);

        let expected = vec![0.75, 1.5, 2.25];

        let result: Vec<f32> = wcl(&high, &low, &close).into();

        assert_eq!(result, expected);
    }
}
