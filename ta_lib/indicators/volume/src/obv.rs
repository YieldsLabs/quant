use core::prelude::*;

pub fn obv(source: &Price, volume: &Price) -> Price {
    (source.change(1).nz(Some(ZERO)).sign() * volume).cumsum()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_obv() {
        let close = Series::from([
            7.7975, 7.8065, 7.817, 7.831, 7.82, 7.826, 7.837, 7.844, 7.8655,
        ]);

        let volume = Series::from([
            3798.0, 5415.0, 7110.0, 2172.0, 7382.0, 2755.0, 2130.0, 21988.0, 9441.0,
        ]);

        let expected = [
            3798.0, 9213.0, 16323.0, 18495.0, 11113.0, 13868.0, 15998.0, 37986.0, 47427.0,
        ];

        let result: Vec<Scalar> = obv(&close, &volume).into();

        assert_eq!(result, expected);
    }
}
