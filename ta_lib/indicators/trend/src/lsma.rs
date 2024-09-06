use core::prelude::*;

pub fn lsma(source: &Price, period: Period) -> Price {
    source.smooth(Smooth::LSMA, period)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_lsma() {
        let source = Series::from([
            12.529, 12.504, 12.517, 12.542, 12.547, 12.577, 12.539, 12.577, 12.490, 12.490,
        ]);
        let expected = vec![
            12.529, 12.504, 12.510668, 12.54, 12.550336, 12.572831, 12.550328, 12.564322,
            12.510831, 12.475489,
        ];

        let result: Vec<Scalar> = lsma(&source, 3).into();

        assert_eq!(result, expected);
    }
}
