use core::Series;

pub fn tma(source: &Series<f32>, period: usize) -> Series<f32> {
    let sma = source.ma(period);

    sma.ma(period)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_tma() {
        let source = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let expected = vec![1.0, 1.25, 1.5, 2.1666667, 3.0];

        let result: Vec<f32> = tma(&source, 3).into();

        assert_eq!(result, expected);
    }
}
