use overlap::ema::ema;

pub fn zlema(source: &[f64], period: usize) -> Vec<Option<f64>> {
    let len = source.len();

    let lag = (period - 1) / 2;

    let mut ema_data = vec![0.0; len];
    let mut zlema = vec![None; len];

    for i in 0..len {
        if i >= lag {
            let price = source[i];
            let prev_price = source[i - lag];
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
        let source = vec![100.0, 105.0, 110.0, 115.0, 120.0];
        let period = 3;
        let expected = vec![None, None, Some(85.0), Some(102.5), Some(113.75)];

        let result = zlema(&source, period);

        assert_eq!(result, expected);
    }
}
