use crate::kb;
use core::prelude::*;

pub fn kbp(source: &Series<f32>, period: usize, factor: f32) -> Series<f32> {
    let (upb, _, lb) = kb(source, period, factor);

    (source - &lb) / (upb - &lb)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_kbp() {
        let source = Series::from([2.0, 4.0, 6.0, 8.0, 10.0, 9.0, 8.0, 7.0, 6.0, 5.0]);
        let period = 3;
        let factor = 2.0;
        let expected = [
            0.0, 0.75, 0.80618626, 0.80618614, 0.80618614, 0.5, 0.3469068, 0.19381316, 0.19381405,
            0.19381405,
        ];

        let result: Vec<f32> = kbp(&source, period, factor).into();

        assert_eq!(result, expected);
    }
}
