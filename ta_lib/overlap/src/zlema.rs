use crate::ema::ema;

pub fn zlema(close: &[f64], period: usize) -> Vec<Option<f64>> {
    let len = close.len();

    let lag = (period - 1) / 2;

    let mut ema_data = vec![0.0; len];
    let mut zlema = vec![None; len];

    for i in 0..len {
        if i >= lag {
            let price = close[i];
            let prev_price = close[i - lag];
            ema_data[i] = price + (price - prev_price);
        }
    }

    let ema_result = ema(&ema_data, period);

    for i in 0..len {
        if i >= lag {
            zlema[i] = ema_result[i];
        }
    }

    zlema
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_zlema() {
        let close = vec![100.0, 105.0, 110.0, 115.0, 120.0];
        let period = 3;
        let expected = vec![None, None, Some(85.0), Some(102.5), Some(113.75)];

        let result = zlema(&close, period);

        assert_eq!(result, expected);
    }
}
