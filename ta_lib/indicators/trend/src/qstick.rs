use core::Series;

pub fn qstick(open: &Series<f32>, close: &Series<f32>, period: usize) -> Series<f32> {
    (close - open).ema(period)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_qstick() {
        let open = Series::from([19.310, 19.316, 19.347, 19.355, 19.386]);
        let close = Series::from([6.8445, 6.8560, 6.8565, 6.8590, 6.8530]);
        let period = 3;
        let expected = vec![-12.4655, -12.4627495, -12.4766245, -12.486312, -12.509655];

        let result: Vec<f32> = qstick(&open, &close, period).into();

        assert_eq!(result, expected);
    }
}
