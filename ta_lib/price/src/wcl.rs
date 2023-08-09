use core::series::Series;

pub fn wcl(high: &[f32], low: &[f32], close: &[f32]) -> Vec<f32> {
    let high = Series::from(high);
    let low = Series::from(low);
    let close = Series::from(close);

    let wcl = (high + low + (close * 2.0)) / 4.0;

    wcl.into()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_weighted_close_price() {
        let high = vec![1.0, 2.0, 3.0];
        let low = vec![0.5, 1.0, 1.5];
        let close = vec![0.75, 1.5, 2.25];
        let expected = vec![0.75, 1.5, 2.25];

        let result = wcl(&high, &low, &close);

        assert_eq!(result, expected);
    }
}
