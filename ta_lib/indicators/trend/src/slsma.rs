use core::prelude::*;

pub fn slsma(source: &Price, period: Period) -> Price {
    let lsma = source.smooth(Smooth::LSMA, period);

    &lsma - (&lsma - lsma.smooth(Smooth::LSMA, period))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_slsma() {
        let source = Series::from([
            12.529, 12.504, 12.517, 12.542, 12.547, 12.577, 12.539, 12.577, 12.490, 12.490,
        ]);
        let expected = vec![
            12.529, 12.504, 12.50539, 12.536224, 12.553506, 12.570806, 12.557826, 12.558236,
            12.522075, 12.472454,
        ];

        let result: Vec<Scalar> = slsma(&source, 3).into();

        assert_eq!(result, expected);
    }
}
