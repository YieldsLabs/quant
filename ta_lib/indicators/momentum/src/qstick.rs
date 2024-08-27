use core::prelude::*;

pub fn qstick(open: &Price, close: &Price, smooth_type: Smooth, period: Period) -> Price {
    (close - open).smooth(smooth_type, period)
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

        let result: Vec<f32> = qstick(&open, &close, Smooth::EMA, period).into();

        assert_eq!(result, expected);
    }
}
