use core::series::Series;

pub fn dema(source: &[f32], period: usize) -> Series<f32> {
    let source = Series::from(source);

    let ema1 = source.ema(period);
    let ema2 = ema1.ema(period);

    

    2.0 * ema1 - ema2
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_dema() {
        let source = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let expected = vec![1.0, 1.75, 2.75, 3.8125, 4.875];

        let result: Vec<f32> = dema(&source, 3).into();

        assert_eq!(result, expected);
    }
}
