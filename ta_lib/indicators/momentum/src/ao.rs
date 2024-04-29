use core::prelude::*;

pub fn ao(
    source: &Series<f32>,
    smooth_type: Smooth,
    fast_period: usize,
    slow_period: usize,
) -> Series<f32> {
    source.smooth(smooth_type, fast_period) - source.smooth(smooth_type, slow_period)
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
        let fast_period = 2;
        let slow_period = 4;
        let expected = vec![0.0, 0.0, 0.5, 1.0, 1.0];

        let result: Vec<f32> = ao(&hl2, Smooth::SMA, fast_period, slow_period).into();

        assert_eq!(result, expected);
    }
}
