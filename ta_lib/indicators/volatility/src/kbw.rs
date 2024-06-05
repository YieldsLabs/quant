use crate::kb;
use core::prelude::*;

pub fn kbw(source: &Series<f32>, period: usize, factor: f32) -> Series<f32> {
    let (upb, mb, lb) = kb(source, period, factor);

    SCALE * (upb - lb) / mb
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_kbw() {
        let source = Series::from([2.0, 4.0, 6.0, 8.0, 10.0, 9.0, 8.0, 7.0, 6.0, 5.0]);
        let period = 3;
        let factor = 2.0;
        let expected = [
            0.0, 133.33333, 163.2993, 108.86625, 81.64969, 72.5775, 72.57743, 40.824745, 46.65699,
            54.433155,
        ];

        let result: Vec<f32> = kbw(&source, period, factor).into();

        assert_eq!(result, expected);
    }
}
