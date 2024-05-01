use core::prelude::*;

pub fn kama(source: &Series<f32>, period: usize) -> Series<f32> {
    source.smooth(Smooth::KAMA, period)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_kama() {
        let source = Series::from([
            5.0788, 5.0897, 5.0958, 5.1023, 5.0998, 5.1046, 5.1014, 5.1141, 5.1355, 5.1477, 5.1675,
            5.2000, 5.2169,
        ]);
        let expected = vec![
            0.0, 0.0, 0.0, 5.1023, 5.1018033, 5.1023088, 5.102306, 5.104807, 5.1141686, 5.129071,
            5.1461506, 5.1700835, 5.190891,
        ];

        let result: Vec<f32> = kama(&source, 3).into();

        assert_eq!(result, expected);
    }
}
