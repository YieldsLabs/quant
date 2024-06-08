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

pub fn fpp(
    high: &Series<f32>,
    low: &Series<f32>,
    close: &Series<f32>,
) -> (Series<f32>, Series<f32>) {
    let pp = (high + low + close) / 3.;

    let hl = 0.382 * (high - low);

    let support = &pp - &hl;
    let resistance = &pp + &hl;

    (support, resistance)
}

pub fn spp(
    high: &Series<f32>,
    low: &Series<f32>,
    close: &Series<f32>,
    smooth_type: Smooth,
    period: usize,
) -> (Series<f32>, Series<f32>) {
    let hh = high.highest(period);
    let ll = low.lowest(period);
    let close = close.smooth(smooth_type, period);

    let pp = (&hh + &ll + close) / 3.;

    let support = 2. * pp.lowest(period) - hh;
    let resistance = 2. * pp.highest(period) - ll;

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

    #[test]
    fn test_fibonacci_pivot_points() {
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
            6.545014, 6.554479, 6.5285473, 6.4801064, 6.5000324, 6.526498, 6.5133805, 6.5214005,
            6.527384, 6.522512, 6.4983974, 6.455343, 6.4681735, 6.481808, 6.49627, 6.5122905,
        ];
        let expected_resistance = vec![
            6.5589185, 6.6045213, 6.5775194, 6.5380936, 6.531968, 6.569969, 6.551886, 6.535,
            6.549616, 6.5416884, 6.5246024, 6.4939246, 6.4874263, 6.5381913, 6.51453, 6.5297093,
        ];

        let (support, resistance) = fpp(&high, &low, &close);
        let result_support: Vec<f32> = support.into();
        let result_resistance: Vec<f32> = resistance.into();

        assert_eq!(result_support, expected_support);
        assert_eq!(result_resistance, expected_resistance);
    }

    #[test]
    fn test_smooth_pivot_points() {
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

        let expected_support = vec![
            6.5439324, 6.4990325, 6.4990325, 6.4780555, 6.467311, 6.4813333, 6.4813333, 6.4813333,
            6.5010676, 6.518056, 6.498766, 6.452577, 6.448855, 6.427755, 6.427755, 6.440223,
        ];
        let expected_resistance = vec![
            6.5621324, 6.6062336, 6.615534, 6.6674337, 6.6524887, 6.6047554, 6.5758677, 6.5677786,
            6.5677786, 6.5619783, 6.5738664, 6.611756, 6.592466, 6.544577, 6.5471992, 6.55031,
        ];

        let (support, resistance) = spp(&high, &low, &close, Smooth::SMA, period);
        let result_support: Vec<f32> = support.into();
        let result_resistance: Vec<f32> = resistance.into();

        assert_eq!(result_support, expected_support);
        assert_eq!(result_resistance, expected_resistance);
    }
}
