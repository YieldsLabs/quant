use crate::stoch;
use core::Series;

pub fn stc(
    close: &Series<f32>,
    fast_period: usize,
    slow_period: usize,
    cycle: usize,
    d_first: usize,
    d_second: usize,
) -> Series<f32> {
    let macd_line = close.ema(fast_period) - close.ema(slow_period);
    let k = stoch(&macd_line, &macd_line, &macd_line, cycle);
    let d = k.ema(d_first);
    let kd = stoch(&d, &d, &d, cycle);

    kd.ema(d_second)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_stc() {
        let source = Series::from([
            1.3626, 1.3630, 1.3637, 1.3653, 1.3692, 1.3689, 1.3719, 1.3715, 1.3732, 1.3701, 1.3730,
            1.3742,
        ]);
        let fast_period = 2;
        let slow_period = 3;
        let cycle = 2;
        let d_first = 3;
        let d_second = 3;
        let expected = vec![
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 50.0, 25.0, 62.5, 31.25, 65.625, 82.8125,
        ];

        let result: Vec<f32> =
            stc(&source, fast_period, slow_period, cycle, d_first, d_second).into();

        assert_eq!(result, expected);
    }
}
