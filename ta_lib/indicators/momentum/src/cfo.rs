use core::prelude::*;

pub fn cfo(source: &Price, period: Period) -> Price {
    SCALE * (source - source.smooth(Smooth::LSMA, period)) / source
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_cfo() {
        let source = Series::from([
            2.0846, 2.0881, 2.0889, 2.0896, 2.0875, 2.0904, 2.0909, 2.0936,
        ]);
        let expected = vec![
            0.0,
            0.0,
            -0.021537453,
            -0.0008100937,
            -0.022374226,
            0.039839078,
            -0.019179303,
            0.017605804,
        ];

        let result: Vec<Scalar> = cfo(&source, 3).into();

        assert_eq!(result, expected);
    }
}
