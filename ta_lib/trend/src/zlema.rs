use core::series::Series;

pub fn zlema(source: &[f64], period: usize) -> Vec<f64> {
    let source = Series::from(source);

    let ema_first = source.ema(period);
    let ema_second = ema_first.ema(period);

    let macd_line = &ema_first - &ema_second;

    let zlema = ema_first + &macd_line;

    zlema.into()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_zlema() {
        let source = vec![100.0, 105.0, 110.0, 115.0, 120.0];
        let period = 3;
        let expected = vec![100.0, 103.75, 108.75, 114.0625, 119.375];

        let result = zlema(&source, period);

        assert_eq!(result, expected);
    }
}
