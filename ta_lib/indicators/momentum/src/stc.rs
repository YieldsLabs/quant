use crate::stoch;
use core::{iff, Series};

pub fn stc(
    close: &Series<f32>,
    fast_period: usize,
    slow_period: usize,
    period: usize,
    factor: f32,
) -> Series<f32> {
    let macd_line = close.ema(fast_period) - close.ema(slow_period);
    let k = stoch(&macd_line, &macd_line, &macd_line, period);

    let len = close.len();
    let mut d = Series::zero(len);

    for _ in 0..len {
        let prev_d = d.shift(1);

        d = iff!(prev_d.na(), k, &prev_d + factor * (&k - &prev_d));
    }

    let kd = stoch(&d, &d, &d, period);

    let mut stc = Series::zero(len);

    for _ in 0..len {
        let prev_stc = stc.shift(1);

        stc = iff!(prev_stc.na(), kd, &prev_stc + factor * (&kd - &prev_stc));
    }

    stc
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
        let period = 2;
        let factor = 0.5;
        let expected = vec![
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 50.0, 25.0, 62.5, 31.25, 65.625, 82.8125,
        ];

        let result: Vec<f32> = stc(&source, fast_period, slow_period, period, factor).into();

        assert_eq!(result, expected);
    }
}
