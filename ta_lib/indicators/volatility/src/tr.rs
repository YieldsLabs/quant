use core::prelude::*;

pub fn tr(high: &Series<f32>, low: &Series<f32>, close: &Series<f32>) -> Series<f32> {
    let prev_close = close.shift(1);
    let diff = high - low;

    iff!(
        high.shift(1).na(),
        diff,
        diff.max(&(high - &prev_close).abs())
            .max(&(low.negate() + &prev_close).abs())
    )
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_true_range() {
        let high = Series::from([50.0, 60.0, 55.0, 70.0]);
        let low = Series::from([40.0, 50.0, 45.0, 60.0]);
        let close = Series::from([45.0, 55.0, 50.0, 65.0]);
        let expected = vec![10.0, 15.0, 10.0, 20.0];

        let result: Vec<f32> = tr(&high, &low, &close).into();

        assert_eq!(result, expected);
    }
}
