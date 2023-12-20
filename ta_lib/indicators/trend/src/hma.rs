use core::prelude::*;

pub fn hma(source: &Series<f32>, period: usize) -> Series<f32> {
    source.hma(period)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_hma() {
        let source = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let expected = vec![0.0, 0.0, 3.0000002, 4.0, 4.9999995];

        let result: Vec<f32> = hma(&source, 3).into();

        assert_eq!(result, expected);
    }
}
