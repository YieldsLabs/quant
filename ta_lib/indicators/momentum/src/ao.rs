use core::prelude::*;

pub fn ao(hl2: &Series<f32>, short_period: usize, long_period: usize) -> Series<f32> {
    hl2.smooth(Smooth::SMA, short_period) - hl2.smooth(Smooth::SMA, long_period)
}

#[cfg(test)]
mod tests {
    use super::*;
    use price::prelude::*;

    #[test]
    fn test_ao() {
        let high = Series::from([3.0, 4.0, 5.0, 6.0, 7.0]);
        let low = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let hl2 = median_price(&high, &low);
        let short_period = 2;
        let long_period = 4;
        let expected = vec![0.0, 0.0, 0.5, 1.0, 1.0];

        let result: Vec<f32> = ao(&hl2, short_period, long_period).into();

        assert_eq!(result, expected);
    }
}
