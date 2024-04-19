use crate::tr;
use core::prelude::*;

pub fn atr(
    high: &Series<f32>,
    low: &Series<f32>,
    close: &Series<f32>,
    smooth_type: Smooth,
    period: usize,
) -> Series<f32> {
    tr(high, low, close).smooth(smooth_type, period)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_atr_smma() {
        let high = Series::from([
            6.5600, 6.6049, 6.5942, 6.5541, 6.5300, 6.5700, 6.5630, 6.5362, 6.5497, 6.5480, 6.5325,
            6.5065, 6.4866, 6.5536, 6.5142, 6.5294,
        ]);
        let low = Series::from([
            6.5418, 6.5394, 6.5301, 6.4782, 6.4882, 6.5131, 6.5126, 6.5184, 6.5206, 6.5229, 6.4982,
            6.4560, 6.4614, 6.4798, 6.4903, 6.5066,
        ]);
        let close = Series::from([
            6.5541, 6.5942, 6.5348, 6.4950, 6.5298, 6.5616, 6.5223, 6.5300, 6.5452, 6.5254, 6.5038,
            6.4614, 6.4854, 6.4966, 6.5117, 6.5270,
        ]);
        let period = 3;
        let expected = [
            0.01819992,
            0.03396654,
            0.044011116,
            0.05464077,
            0.05036052,
            0.05254035,
            0.051826984,
            0.040484603,
            0.036689714,
            0.032826394,
            0.033317544,
            0.039045,
            0.03442996,
            0.047553174,
            0.03966879,
            0.03404585,
        ];

        let result: Vec<f32> = atr(&high, &low, &close, Smooth::SMMA, period).into();

        assert_eq!(result, expected);
    }
}
