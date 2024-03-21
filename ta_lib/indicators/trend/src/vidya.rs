use core::prelude::*;

pub fn vidya(source: &Series<f32>, period: usize, alpha: f32) -> Series<f32> {
    let alpha = alpha / source.std(period).smooth(Smooth::WMA, period);
    let ema = source.smooth(Smooth::EMA, period);

    &ema + alpha * (source - &ema)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_vidya() {
        let source = Series::from([18.898, 18.838, 18.881, 18.925, 18.846]);
        let period = 3;
        let alpha = 0.2;
        let expected = vec![0.0, 0.0, 18.93209, 19.063356, 18.704758];

        let result: Vec<f32> = vidya(&source, period, alpha).into();

        assert_eq!(result, expected);
    }
}
