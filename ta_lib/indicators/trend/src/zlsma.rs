use core::prelude::*;

pub fn zlsma(source: &Price, period: Period) -> Price {
    let lsma = source.smooth(Smooth::LSMA, period);

    2. * &lsma - lsma.smooth(Smooth::LSMA, period)
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
            12.529, 12.504, 12.515945, 12.543776, 12.547166, 12.574857, 12.54283, 12.570409,
            12.499587, 12.478523,
        ];

        let result: Vec<Scalar> = zlsma(&source, 3).into();

        assert_eq!(result, expected);
    }
}
