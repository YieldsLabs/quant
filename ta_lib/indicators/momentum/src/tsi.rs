use core::prelude::*;

pub fn tsi(source: &Price, smooth: Smooth, period_slow: Period, period_fast: Period) -> Price {
    let pc = source.change(1);

    let pcds = pc.smooth(smooth, period_slow).smooth(smooth, period_fast);
    let apcds = pc
        .abs()
        .smooth(smooth, period_slow)
        .smooth(smooth, period_fast);

    SCALE * pcds / apcds
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_tsi() {
        let source = Series::from([
            6.858, 6.86, 6.8480, 6.8575, 6.864, 6.8565, 6.8455, 6.8450, 6.8365, 6.8310, 6.8355,
            6.8360, 6.8345, 6.8285, 6.8395,
        ]);
        let slow_period = 3;
        let fast_period = 2;
        let expected = vec![
            0.0,
            100.0,
            -49.99404,
            8.398337,
            42.496567,
            -0.019883709,
            -48.616287,
            -59.83348,
            -79.84944,
            -89.061806,
            -40.238903,
            -20.758427,
            -28.600376,
            -69.15327,
            27.16367,
        ];

        let result: Vec<Scalar> = tsi(&source, Smooth::EMA, slow_period, fast_period).into();

        assert_eq!(result, expected);
    }
}
