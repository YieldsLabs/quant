use crate::roc;
use core::prelude::*;

pub fn trix(source: &Price, smooth: Smooth, period: Period) -> Price {
    let ema3 = source
        .smooth(smooth, period)
        .smooth(smooth, period)
        .smooth(smooth, period);

    SCALE * roc(&ema3, 1)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_trix() {
        let source = Series::from([
            6.858, 6.86, 6.8480, 6.8575, 6.864, 6.8565, 6.8455, 6.8450, 6.8365, 6.8310, 6.8355,
            6.8360, 6.8345, 6.8285, 6.8395,
        ]);
        let period = 3;
        let expected = vec![
            0.0, 0.36433753, -1.6401544, -1.002056, 0.9569516, 0.61472696, -1.9254234, -3.3216302,
            -5.0126247, -6.273622, -5.246739, -3.7003598, -2.672774, -2.9872787, -0.9277002,
        ];

        let result: Vec<f32> = trix(&source, Smooth::EMA, period).into();

        assert_eq!(result, expected);
    }
}
