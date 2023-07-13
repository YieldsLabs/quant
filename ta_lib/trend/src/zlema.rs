use core::series::Series;
use overlap::ema::ema;

pub fn zlema(source: &[f64], period: usize) -> Series<f64> {
    let ema_first = ema(source, period);
    let ema_first_vec: Vec<f64> = ema_first.clone().into();

    let ema_second = ema(&ema_first_vec, period);

    let diff = &ema_first - &ema_second;

    let zlema = ema_first + &diff;

    zlema
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_zlema() {
        let source = vec![100.0, 105.0, 110.0, 115.0, 120.0];
        let period = 3;
        let expected = vec![
            Some(100.0),
            Some(103.75),
            Some(108.75),
            Some(114.0625),
            Some(119.375),
        ];

        let result = zlema(&source, period);

        assert_eq!(result, expected);
    }
}
