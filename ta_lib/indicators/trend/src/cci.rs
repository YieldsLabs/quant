use core::series::Series;

pub fn cci(hlc3: &[f32], period: usize, factor: f32) -> Series<f32> {
    let hlc3 = Series::from(hlc3);
    
    let cci = (&hlc3 - &hlc3.ma(period)) / (factor * hlc3.md(period));

    cci
}

#[cfg(test)]
mod tests {
    use super::*;
    use price::typical_price;

    #[test]
    fn test_cci() {
        let high = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let low = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let close = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let hlc3 = typical_price(&high, &low, &close);
        let expected = vec![0.0, 66.66667, 100.0, 100.0, 100.0];

        let result: Vec<f32> = cci(&hlc3, 3, 0.015).into();

        assert_eq!(result, expected);
    }
}
