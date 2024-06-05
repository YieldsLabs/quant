use crate::kch;
use core::prelude::*;

pub fn kchp(
    source: &Series<f32>,
    atr: &Series<f32>,
    smooth_type: Smooth,
    period: usize,
    factor: f32,
) -> Series<f32> {
    let (upb, _, lb) = kch(source, atr, smooth_type, period, factor);

    (source - &lb) / (upb - &lb)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::atr;
    use price::prelude::*;

    #[test]
    fn test_kchp() {
        let close = Series::from([
            19.102, 19.100, 19.146, 19.181, 19.155, 19.248, 19.309, 19.355, 19.439,
        ]);
        let high = Series::from([
            19.129, 19.116, 19.154, 19.195, 19.217, 19.285, 19.341, 19.394, 19.450,
        ]);
        let low = Series::from([
            19.090, 19.086, 19.074, 19.145, 19.141, 19.155, 19.219, 19.306, 19.355,
        ]);
        let period = 3;
        let atr_period = 3;
        let atr = atr(&high, &low, &close, Smooth::SMMA, atr_period);
        let hlc3 = typical_price(&high, &low, &close);
        let factor = 2.0;
        let expected = [
            0.5, 0.47801208, 0.5513957, 0.6472284, 0.55733025, 0.6086896, 0.6256523, 0.64774823,
            0.6573705,
        ];

        let result: Vec<f32> = kchp(&hlc3, &atr, Smooth::EMA, period, factor).into();

        assert_eq!(result, expected);
    }
}
