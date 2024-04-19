use core::prelude::*;

pub fn tr(high: &Series<f32>, low: &Series<f32>, close: &Series<f32>) -> Series<f32> {
    let prev_close = close.shift(1);
    let diff = high - low;

    iff!(
        high.shift(1).na(),
        diff,
        diff.max(&(high - &prev_close).abs())
            .max(&(low - &prev_close).abs())
    )
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_true_range() {
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
        let expected = vec![
            0.01819992,
            0.06549978,
            0.064100266,
            0.07590008,
            0.041800022,
            0.056900024,
            0.050400257,
            0.017799854,
            0.029099941,
            0.025099754,
            0.03429985,
            0.050499916,
            0.02519989,
            0.07379961,
            0.023900032,
            0.022799969,
        ];

        let result: Vec<f32> = tr(&high, &low, &close).into();

        assert_eq!(result, expected);
    }
}
