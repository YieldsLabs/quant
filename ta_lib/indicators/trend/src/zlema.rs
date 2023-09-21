use core::series::Series;

pub fn zlema(source: &[f32], period: usize) -> Series<f32> {
    let source = Series::from(source);
    let lag = (period as f32 / 2.0).round() as usize;

    let d = (2.0 * &source) - source.shift(lag);
    let zlema = d.ema(period);

    zlema
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_zlema() {
        let source = vec![18.898, 18.838, 18.881, 18.925, 18.846];
        let period = 3;
        let expected = vec![0.0, 0.0, 18.864, 18.938, 18.8745];

        let result: Vec<f32> = zlema(&source, period).into();

        assert_eq!(result, expected);
    }
}
