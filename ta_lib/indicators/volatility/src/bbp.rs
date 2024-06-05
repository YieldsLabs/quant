use crate::bb;
use core::prelude::*;

pub fn bbp(source: &Series<f32>, smooth_type: Smooth, period: usize, factor: f32) -> Series<f32> {
    let (upb, _, lb) = bb(source, smooth_type, period, factor);

    (source - &lb) / (upb - &lb)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_bbp() {
        let source = Series::from([2.0, 4.0, 6.0, 8.0, 10.0, 9.0, 8.0, 7.0, 6.0, 5.0]);
        let period = 3;
        let factor = 2.0;
        let expected = [
            0.0, 0.75, 0.80618626, 0.80618614, 0.8061864, 0.5, 0.19381316, 0.19381316, 0.19381405,
            0.19381405,
        ];
        let result: Vec<f32> = bbp(&source, Smooth::SMA, period, factor).into();

        assert_eq!(result, expected);
    }
}
