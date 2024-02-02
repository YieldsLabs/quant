use core::prelude::*;

pub fn sma(source: &Series<f32>, period: usize) -> Series<f32> {
    source.smooth(Smooth::SMA, period)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_sma() {
        let source = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let expected = vec![1.0, 1.5, 2.0, 3.0, 4.0];

        let result: Vec<f32> = sma(&source, 3).into();

        assert_eq!(result, expected);
    }
}
