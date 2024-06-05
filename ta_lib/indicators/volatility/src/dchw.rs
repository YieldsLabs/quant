use crate::dch;
use core::prelude::*;

pub fn dchw(high: &Series<f32>, low: &Series<f32>, period: usize) -> Series<f32> {
    let (upb, _, lb) = dch(high, low, period);

    upb - lb
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_dchw() {
        let high = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let low = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let period = 3;

        let expected = vec![0.0, 1.0, 2.0, 2.0, 2.0];

        let result: Vec<f32> = dchw(&high, &low, period).into();

        assert_eq!(result, expected);
    }
}
