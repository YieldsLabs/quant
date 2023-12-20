use core::prelude::*;

pub fn lsma(source: &Series<f32>, period: usize) -> Series<f32> {
    source.linreg(period)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_lsma() {
        let source = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let expected = vec![0.0, 2.0, 3.0000002, 4.0, 5.0];

        let result: Vec<f32> = lsma(&source, 3).into();

        assert_eq!(result, expected);
    }
}
