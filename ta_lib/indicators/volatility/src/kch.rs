use core::prelude::*;

pub fn kch(
    source: &Series<f32>,
    smooth: Smooth,
    atr: &Series<f32>,
    period: usize,
    factor: f32,
) -> (Series<f32>, Series<f32>, Series<f32>) {
    let middle_band = source.smooth(smooth, period);
    let volatility = factor * atr;

    let upper_band = &middle_band + &volatility;
    let lower_band = &middle_band - &volatility;

    (upper_band, middle_band, lower_band)
}

pub fn kchp(
    source: &Series<f32>,
    smooth: Smooth,
    atr: &Series<f32>,
    period: usize,
    factor: f32,
) -> Series<f32> {
    let (upb, _, lb) = kch(source, smooth, atr, period, factor);

    (source - &lb) / (upb - lb)
}

pub fn kchw(
    source: &Series<f32>,
    smooth: Smooth,
    atr: &Series<f32>,
    period: usize,
    factor: f32,
) -> Series<f32> {
    let (upb, mb, lb) = kch(source, smooth, atr, period, factor);

    SCALE * (upb - lb) / mb
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::atr;
    use price::prelude::*;

    #[test]
    fn test_kch() {
        let high = Series::from([
            19.129, 19.116, 19.154, 19.195, 19.217, 19.285, 19.341, 19.394, 19.450,
        ]);
        let low = Series::from([
            19.090, 19.086, 19.074, 19.145, 19.141, 19.155, 19.219, 19.306, 19.355,
        ]);
        let close = Series::from([
            19.102, 19.100, 19.146, 19.181, 19.155, 19.248, 19.309, 19.355, 19.439,
        ]);
        let period = 3;
        let atr_period = 3;
        let atr = atr(&high, &low, &close, Smooth::SMMA, atr_period);
        let hlc3 = typical_price(&high, &low, &close);
        let factor = 2.0;
        let epsilon = 0.001;
        let expected_upper_band = [
            19.185, 19.175833, 19.215582, 19.244846, 19.275402, 19.358686, 19.433056, 19.482948,
            19.543198,
        ];
        let expected_middle_band = [
            19.107, 19.103834, 19.11425, 19.143959, 19.157478, 19.193405, 19.241535, 19.2966,
            19.355633,
        ];
        let expected_lower_band = [
            19.029001, 19.031836, 19.012918, 19.043072, 19.039555, 19.028124, 19.050014, 19.110252,
            19.168068,
        ];

        let (upper_band, middle_band, lower_band) = kch(&hlc3, Smooth::EMA, &atr, period, factor);

        let result_upper_band: Vec<f32> = upper_band.into();
        let result_middle_band: Vec<f32> = middle_band.into();
        let result_lower_band: Vec<f32> = lower_band.into();

        for i in 0..high.len() {
            let a = result_upper_band[i];
            let b = expected_upper_band[i];
            assert!((a - b).abs() < epsilon, "at position {}: {} != {}", i, a, b);

            let a = result_middle_band[i];
            let b = expected_middle_band[i];
            assert!((a - b).abs() < epsilon, "at position {}: {} != {}", i, a, b);

            let a = result_lower_band[i];
            let b = expected_lower_band[i];
            assert!((a - b).abs() < epsilon, "at position {}: {} != {}", i, a, b);
        }
    }

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

        let result: Vec<f32> = kchp(&hlc3, Smooth::EMA, &atr, period, factor).into();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_kchw() {
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
            0.8164454, 0.7537607, 1.060274, 1.0539857, 1.2310988, 1.7222717, 1.9907007, 1.9314072,
            1.9380906,
        ];

        let result: Vec<f32> = kchw(&hlc3, Smooth::EMA, &atr, period, factor).into();

        assert_eq!(result, expected);
    }
}
