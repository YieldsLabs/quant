use core::prelude::*;

pub fn vidya(source: &Price, period_fast: Period, period_slow: Period) -> Price {
    let k = source.std(period_fast) / source.std(period_slow);
    let alpha = 2. / ((period_fast + 1) as Scalar) * k.nz(Some(ZERO));

    source.ew(&alpha, source)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_vidya() {
        let source = Series::from([100.0, 105.0, 116.25, 123.125, 129.0625]);
        let fast_period = 2;
        let slow_period = 3;
        let expected = vec![100.0, 103.33333, 110.46114, 114.34566, 119.90917];

        let result: Vec<Scalar> = vidya(&source, fast_period, slow_period).into();

        assert_eq!(result, expected);
    }
}
