use core::prelude::*;

pub fn cmf(
    high: &Series<f32>,
    low: &Series<f32>,
    close: &Series<f32>,
    volume: &Series<f32>,
    period: usize,
) -> Series<f32> {
    let mfv = iff!(
        (close.seq(high) & close.seq(low)) | high.seq(low),
        Series::zero(close.len()),
        ((2. * close - low - high) / (high - low)) * volume
    );

    mfv.sum(period) / volume.sum(period)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_cmf() {
        let high = Series::from([
            19.129, 19.116, 19.154, 19.195, 19.217, 19.285, 19.341, 19.394, 19.450,
        ]);
        let low = Series::from([
            19.090, 19.086, 19.074, 19.145, 19.141, 19.155, 19.219, 19.306, 19.355,
        ]);
        let close = Series::from([
            19.102, 19.100, 19.146, 19.181, 19.155, 19.248, 19.309, 19.355, 19.439,
        ]);
        let volume = Series::from([
            3798.0, 5415.0, 7110.0, 2172.0, 7382.0, 2755.0, 2130.0, 21988.0, 9441.0,
        ]);
        let period = 3;
        let expected = [
            -0.384653,
            -0.19773456,
            0.23686658,
            0.42749897,
            0.1189091,
            -0.20471762,
            -0.2007745,
            0.17482524,
            0.32079986,
        ];

        let result: Vec<f32> = cmf(&high, &low, &close, &volume, period).into();

        assert_eq!(result, expected);
    }
}
