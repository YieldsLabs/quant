use core::prelude::*;

pub fn kama(source: &Price, period: Period) -> Price {
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
            5.0788, 5.0788455, 5.078916, 5.0892878, 5.0915785, 5.0941925, 5.09429, 5.0988545,
            5.110461, 5.1269784, 5.144952, 5.1693687, 5.190451,
        ];

        let result: Vec<Scalar> = kama(&source, 3).into();

        assert_eq!(result, expected);
    }
}
