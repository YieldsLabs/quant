use core::prelude::*;

pub fn pp(
    high: &Series<f32>,
    low: &Series<f32>,
    close: &Series<f32>,
) -> (Series<f32>, Series<f32>) {
    let pp = (high + low + close) / 3.;

    let support = 2. * &pp - high;
    let resistance = 2. * &pp - low;

    (support, resistance)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_pivot_points() {
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
        let expected_support = vec![
            6.5439324, 6.5541005, 6.5118666, 6.4641, 6.5020003, 6.526467, 6.5022664, 6.5202003,
            6.5273, 6.5162005, 6.4905, 6.4427676, 6.469, 6.4663997, 6.4966, 6.5126,
        ];
        let expected_resistance = vec![
            6.5621324, 6.6196003, 6.575967, 6.54, 6.5438004, 6.583367, 6.5526667, 6.538, 6.5564,
            6.5413003, 6.5248, 6.4932675, 6.4941998, 6.5401993, 6.5205, 6.5354,
        ];

        let (support, resistance) = pp(&high, &low, &close);
        let result_support: Vec<f32> = support.into();
        let result_resistance: Vec<f32> = resistance.into();

        assert_eq!(result_support, expected_support);
        assert_eq!(result_resistance, expected_resistance);
    }
}
