use core::prelude::*;

pub fn kama(source: &Series<f32>, period: usize) -> Series<f32> {
    source.smooth(Smooth::KAMA, period)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_kama() {
        let source = Series::from([19.099, 19.079, 19.074, 19.139, 19.191]);
        let expected = vec![19.099, 19.089, 19.081501, 19.112799, 19.173977];

        let result: Vec<f32> = kama(&source, 3).into();

        assert_eq!(result, expected);
    }
}
